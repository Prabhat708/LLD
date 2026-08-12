class Song:
    def __init__(self, title, artist, file_path):
        self.title = title
        self.artist = artist
        self.file_path = file_path

    def get_title(self):
        return self.title

    def get_artist(self):
        return self.artist

    def get_file_path(self):
        return self.file_path
