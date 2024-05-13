import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

model_id = "stabilityai/stable-diffusion-2-1"
image_save_Path = "./Stable-Diffusion-Image.png"
def Generate_Image(prompt):
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")
    Prompt = prompt
    image = pipe(prompt).images[0]
    image.save(image_save_Path)