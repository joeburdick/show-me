import json
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

class StabilityConfig():
    def __init__(self, steps, seed, cfg_scale, sampler: generation.SamplerParameters):
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

    config['sampler']: generation.SamplerParameters[config['sampler']]

    return StabilityConfig(**config)

def save_stability_config(configPath: str, config: StabilityConfig):
    with open(configPath, 'w') as f:
        json.dump(config.__dict__, f)
