from show_me.image_generation.stability_config import get_stability_config

stabilityConfig = get_stability_config()
print(stabilityConfig.to_json())