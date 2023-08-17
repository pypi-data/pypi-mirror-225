from __future__ import annotations

from functools import cached_property

from diffusers import (
    StableDiffusionControlNetInpaintPipeline,
    StableDiffusionControlNetPipeline,
    StableDiffusionInpaintPipeline,
    StableDiffusionPipeline,
)

from noone_pipeline.base import NoOnePipelineBase


class NoOnePipeline(NoOnePipelineBase, StableDiffusionPipeline):
    @cached_property
    def inpaint_pipeline(self):
        return StableDiffusionInpaintPipeline(
            vae=self.vae,
            text_encoder=self.text_encoder,
            tokenizer=self.tokenizer,
            unet=self.unet,
            scheduler=self.scheduler,
            safety_checker=self.safety_checker,
            feature_extractor=self.feature_extractor,
            requires_safety_checker=self.config.requires_safety_checker,
        )

    @property
    def txt2img_class(self):
        return StableDiffusionPipeline


class NoOneCnPipeline(NoOnePipelineBase, StableDiffusionControlNetPipeline):
    @cached_property
    def inpaint_pipeline(self):
        return StableDiffusionControlNetInpaintPipeline(
            vae=self.vae,
            text_encoder=self.text_encoder,
            tokenizer=self.tokenizer,
            unet=self.unet,
            controlnet=self.controlnet,
            scheduler=self.scheduler,
            safety_checker=self.safety_checker,
            feature_extractor=self.feature_extractor,
            requires_safety_checker=self.config.requires_safety_checker,
        )

    @property
    def txt2img_class(self):
        return StableDiffusionControlNetPipeline