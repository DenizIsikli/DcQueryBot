import os


class Setup:
    def __init__(self):
        pass

    @staticmethod
    async def setup_instances(bot, directory, type_name):
        loaded_extensions = []

        try:
            for filename in os.listdir(directory):
                if filename.endswith(".py"):
                    extension_name = f"{directory}.{filename[:-3]}"  # Remove the last 3 characters (.py)
                    try:
                        await bot.load_extension(extension_name)
                        loaded_extensions.append(extension_name)
                    except Exception as e:
                        print(f"Failed to load {type_name} file: {extension_name}: {e}")
        except Exception as e:
            print(f"Failed to load {type_name} files: {e}")

        if loaded_extensions:
            for extension in loaded_extensions:
                print(f"Loaded {type_name} File(s): {extension}")
            print("\n")
