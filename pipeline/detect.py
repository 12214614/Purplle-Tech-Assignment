import cv2
import time
from ultralytics import YOLO
from zones import get_zone
from emit import create_event, emit_event

# -----------------------------
# CONFIG
# -----------------------------
STORE_ID = "STORE_001"

VIDEOS = [
    ("data/CAM_ENTRY_DOOR.mp4", "CAM_ENTRY_DOOR"),
    ("data/CAM_FLOOR_MAIN.mp4", "CAM_FLOOR_MAIN"),
    ("data/CAM_FLOOR_SECONDARY.mp4", "CAM_FLOOR_SECONDARY"),
    ("data/CAM_BILLING_COUNTER.mp4", "CAM_BILLING_COUNTER"),
    # ("data/CAM_BACKROOM.mp4", "CAM_BACKROOM")  # optional ignore
]

ENTRY_LINE_Y = 130
SKIP_FRAMES = 3

# -----------------------------
# LOAD MODEL
# -----------------------------
model = YOLO("yolov8n.pt")
model.conf = 0.4

# -----------------------------
# PROCESS EACH VIDEO
# -----------------------------
for video_path, CAMERA_ID in VIDEOS:

    print(f"Processing {CAMERA_ID}...")
    print(f"\n🎥 Processing: {video_path} | Camera: {CAMERA_ID}")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ Error opening {video_path}")
        continue

    track_history = {}
    seen = {}
    dwell_start = {}
    last_results = []
    frame_count = 0
    start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"✅ Finished: {video_path}")
            break

        frame = cv2.resize(frame, (640, 480))

        if frame_count % SKIP_FRAMES == 0:
            last_results = model.track(frame, persist=True, conf=model.conf, verbose=False)

        results = last_results
        frame_count += 1

        for result in results:
            if result.boxes.id is not None:
                boxes = result.boxes.xyxy
                ids = result.boxes.id

                for box, track_id in zip(boxes, ids):
                    x1, y1, x2, y2 = map(int, box)
                    track_id = int(track_id)

                    # -----------------------------
                    # CENTER POINT
                    # -----------------------------
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    print("CY:", center_y)

                    # -----------------------------
                    # ENTRY / EXIT LOGIC
                    # -----------------------------
                    prev_y = track_history.get(track_id, center_y)

                    if prev_y < ENTRY_LINE_Y and center_y >= ENTRY_LINE_Y:
                        event = create_event(
                            STORE_ID, CAMERA_ID, track_id,
                            "ENTRY", confidence=0.9
                        )
                        emit_event(event)

                    elif prev_y > ENTRY_LINE_Y and center_y <= ENTRY_LINE_Y:
                        event = create_event(
                            STORE_ID, CAMERA_ID, track_id,
                            "EXIT", confidence=0.9
                        )
                        emit_event(event)

                    track_history[track_id] = center_y

                    # -----------------------------
                    # ZONE LOGIC
                    # -----------------------------
                    zone_id = get_zone(center_x, center_y)

                    print("Zone detected:", zone_id)

                    if track_id not in seen:
                        seen[track_id] = set()

                    if zone_id not in seen[track_id]:
                        seen[track_id].add(zone_id)

                        event = create_event(
                            STORE_ID, CAMERA_ID, track_id,
                            "ZONE_ENTER",
                            zone_id=zone_id,
                            confidence=0.9
                        )
                        emit_event(event)

                        dwell_start[track_id] = cv2.getTickCount()

                    # ZONE DWELL
                    if track_id in dwell_start:
                        elapsed = cv2.getTickCount() - dwell_start[track_id]
                        time_sec = elapsed / cv2.getTickFrequency()

                        if time_sec > 5:
                            event = create_event(
                                STORE_ID, CAMERA_ID, track_id,
                                "ZONE_DWELL",
                                zone_id=zone_id,
                                dwell_ms=int(time_sec * 1000),
                                confidence=0.9
                            )
                            emit_event(event)

                            dwell_start[track_id] = cv2.getTickCount()

        if frame_count % 50 == 0:
            print(f"{CAMERA_ID}: {frame_count} frames | time: {round(time.time() - start, 2)}s")

    cap.release()

print("\n🚀 All videos processed successfully!")