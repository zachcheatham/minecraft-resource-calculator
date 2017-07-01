windows = []

# USE THIS TO RETAIN ROOT WINDOWS
# Python will delete them if they aren't referenced somewhere

def retain(window):
    global windows
    windows.append(window)
    window.destroyed.connect(window_destroyed)

def release(window):
    global windows
    window.destroyed.disconnect(window_destroyed)
    windows.remove(window)

def window_destroyed(window):
    print ("[Debug] Retained window destroyed.")
    global windows
    # I feel like this is hella hacky
    for win in windows:
        try:
            win.isVisible()
        except RuntimeError:
            windows.remove(win)
            break
    print ("[Debug] Windows still retained: ")
    print (windows)
