import json
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

class StabilityConfig():
    def __init__(self, steps, seed, cfg_scale, sampler: generation.DiffusionSampler):
        self.steps = steps
        self.seed = seed
        self.cfg_scale = cfg_scale
        self.sampler = sampler

    def to_json(self):
        return json.dumps(self.__dict__)
    
def get_stability_config(configPath: str) -> StabilityConfig:
    # Mapping of string representations to types
    with open(configPath) as f:
        config = json.load(f)

    # set sampler to enum matching string value
    config["sampler"] = generation.DiffusionSampler.Value(config["sampler"])

    # convert number values
    config["steps"] = int(config["steps"])
    config["seed"] = int(config["seed"])
    config["cfg_scale"] = float(config["cfg_scale"])

    return StabilityConfig(**config)

def save_stability_config(configPath: str, config: StabilityConfig):
    with open(configPath, 'w') as f:
        json.dump(config.__dict__, f)
