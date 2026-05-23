from functools import lru_cache


class AmpaFileUploader:
    def upload_ampa_file(self):
        pass


@lru_cache
def get_ampa_file_uploader():
    return AmpaFileUploader()
