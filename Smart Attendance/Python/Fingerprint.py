def fingerprint_listener():
    global waiting_for_fingerprint, recognized_face

    while True:
        try:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode(errors="ignore").strip()

                if line.startswith("FP:"):
                    with lock:
                        currently_waiting = waiting_for_fingerprint
                        face_at_scan_time = recognized_face

                    if not currently_waiting:
                        # No face was verified first - ignore this scan.
                        # Remove this check if you want fingerprint-only mode.
                        print("Fingerprint scanned but no face was verified first - ignoring.")
                        continue

                    fp_id = int(line.split(":")[1])
                    fp_name = fingerprint_map.get(fp_id, f"Unknown_FP_{fp_id}")

                    # --- FIX: cross-check fingerprint owner against the face
                    # that actually triggered this verification window. ---
                    if fp_name.startswith("Unknown_FP_"):
                        print(f"Fingerprint ID {fp_id} is not in fingerprint_map - not marked.")
                        display("Unknown", "fingerprint")

                    elif fp_name != face_at_scan_time:
                        # Someone else's fingerprint was used to confirm this face.
                        print(f"Mismatch: face was '{face_at_scan_time}' but fingerprint "
                              f"belongs to '{fp_name}' - not marked.")
                        display("Mismatch!", "Face/FP differ")

                    else:
                        marked = mark_attendance(fp_name, method="face+fingerprint")
                        if marked:
                            display(f"Welcome {fp_name}", "Attendance Marked")
                        else:
                            display(f"{fp_name}", "Already marked")

                    with lock:
                        waiting_for_fingerprint = False
                        recognized_face = None

                    time.sleep(2)  # let the message stay on screen
                    display("Smart Attendance", "Show your face")

        except Exception as e:
            print("Fingerprint listener error:", e)
        time.sleep(0.1)

fp_thread = threading.Thread(target=fingerprint_listener, daemon=True)
fp_thread.start()