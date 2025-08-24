
import pygame
from tnt import Tnt, MegaTnt, NukeTnt
 
def handle_debug_input(event, space, texture_atlas, atlas_items, sound_manager, camera, tnt_list, pickaxe=None):
    """
    Handles input events for debug mode.
    Does not have its own game loop or drawing logic.
    """
    if event.type == pygame.KEYDOWN:
        # Use pickaxe position if available, else fallback to camera offset
        px = pickaxe.body.position.x if pickaxe is not None else camera.offset_x + 400
        py = pickaxe.body.position.y if pickaxe is not None else camera.offset_y + 100
        if event.key == pygame.K_1:
            tnt = Tnt(space, px, py, texture_atlas, atlas_items, sound_manager, owner_name="debug")
            tnt_list.append(tnt)
            print("Spawned TNT")
        elif event.key == pygame.K_2:
            mega = MegaTnt(space, px, py, texture_atlas, atlas_items, sound_manager, owner_name="debug")
            tnt_list.append(mega)
            print("Spawned MegaTNT")
        elif event.key == pygame.K_3:
            nuke = NukeTnt(space, px, py, texture_atlas, atlas_items, sound_manager, owner_name="debug")
            tnt_list.append(nuke)
            print("Spawned NukeTNT")
        elif event.key == pygame.K_0:
                        import threading
                        from selenium_chat import poll_live_chat_messages_selenium
                        from spawn_requests import enqueue_spawn
                        import json
                        import os

                        # Load settings (editable)
                        settings_path = os.path.join(os.path.dirname(__file__), "chat_settings.json")
                        try:
                            with open(settings_path, "r", encoding="utf-8") as f:
                                settings = json.load(f).get("selenium", {})
                        except Exception:
                            settings = {"poll_interval_seconds": 10, "max_users_per_poll": 5}

                        youtube_url = "https://www.youtube.com/watch?v=BHiPf9JV3eo"  # Or get from config
                        print("Starting Selenium live chat polling from:", youtube_url)

                        def poll_and_enqueue():
                            tnt_queue = []
                            other_queue = []
                            poll_interval = settings.get("poll_interval_seconds", 10)
                            max_users = settings.get("max_users_per_poll", 5)
                            # probabilities (optional use)
                            tnt_chance = settings.get("tnt_chance", 0.9)
                            mega_chance = settings.get("mega_chance", 0.05)
                            nuke_chance = settings.get("nuke_chance", 0.01)
                            other_chance = settings.get("other_chance", 0.04)

                            for messages in poll_live_chat_messages_selenium(youtube_url, poll_interval=poll_interval):
                                # limit users to max_users per poll
                                messages = messages[:max_users]
                                print(f"Polled {len(messages)} new messages from Selenium live chat.")
                                for msg in messages:
                                    author = msg.get("author")
                                    photo = msg.get("photo")
                                    text = msg.get("message", "").lower()
                                    if "tnt" in text:
                                        tnt_queue.append((author, photo, text))
                                    elif any(word in text for word in ["big", "fast", "netherite", "gold", "diamond", "mega", "nuke", "stone", "iron", "wood"]):
                                        other_queue.append((author, photo, text))

                                # Process up to configured numbers per poll, but enqueue spawn requests instead of creating objects here
                                tnt_to_do = tnt_queue[: max(1, int(max_users * tnt_chance))]
                                other_to_do = other_queue[: max(1, int(max_users * (1 - tnt_chance)))]
                                tnt_queue = tnt_queue[len(tnt_to_do):]
                                other_queue = other_queue[len(other_to_do):]

                                # Use pickaxe position if available
                                px = pickaxe.body.position.x if pickaxe is not None else camera.offset_x + 400
                                py = pickaxe.body.position.y if pickaxe is not None else camera.offset_y + 100
                                # Enqueue spawn requests to be handled on main thread
                                for author, photo, text in tnt_to_do:
                                    enqueue_spawn("tnt", px, py, owner_name=author, owner_photo=photo)
                                    try:
                                        # request avatar download in background
                                        from avatar_cache import request as _req_avatar
                                        _req_avatar(photo)
                                    except Exception:
                                        pass
                                    print(f"Enqueued TNT for {author}")
                                for author, photo, text in other_to_do:
                                    if "mega" in text:
                                        enqueue_spawn("mega", px, py, owner_name=author, owner_photo=photo)
                                        try:
                                            from avatar_cache import request as _req_avatar
                                            _req_avatar(photo)
                                        except Exception:
                                            pass
                                        print(f"Enqueued MegaTNT for {author}")
                                    elif "nuke" in text:
                                        enqueue_spawn("nuke", px, py, owner_name=author, owner_photo=photo)
                                        try:
                                            from avatar_cache import request as _req_avatar
                                            _req_avatar(photo)
                                        except Exception:
                                            pass
                                        print(f"Enqueued NukeTNT for {author}")
                                    else:
                                        enqueue_spawn("tnt", px, py, owner_name=author, owner_photo=photo)
                                        try:
                                            from avatar_cache import request as _req_avatar
                                            _req_avatar(photo)
                                        except Exception:
                                            pass
                                        print(f"Enqueued fallback TNT for {author}")

                        threading.Thread(target=poll_and_enqueue, daemon=True).start()
        
