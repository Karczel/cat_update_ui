from cat_ui import CatUI

if __name__ == '__main__':
    # create the UI.  There is no controller (yet), so nothing to inject.
    ui = CatUI('b6510545535/cat')
    ui.run()