class ReadFile:

    @classmethod
    def read_file(cls, file_path):
        try:
            with open(file_path) as f:
                file_data = f.read()
                f.close()
        except FileNotFoundError as e:
            print(e)
            file_data = None
        return file_data
