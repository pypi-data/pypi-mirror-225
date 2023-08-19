# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlight_vision', 'starlight_vision.core']

package_data = \
{'': ['*']}

install_requires = \
['accelerate',
 'beartype',
 'click',
 'datasets',
 'einops>=0.6.1',
 'ema-pytorch>=0.0.3',
 'fsspec',
 'kornia',
 'lion-pytorch',
 'numpy',
 'packaging',
 'pillow',
 'pydantic>=2',
 'pytorch-lightning',
 'pytorch-warmup',
 'sentencepiece',
 'torch>=1.6',
 'torchvision',
 'tqdm',
 'transformers',
 'triton']

setup_kwargs = {
    'name': 'starlight-vision',
    'version': '0.1.1',
    'description': 'Starlight - unprecedented photorealism × deep level of language understanding',
    'long_description': "[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n\n# 🌌 Starlight Vision 🚀\n\n![Starlight](starlight.png)\n🪐 Starlight Vision is a powerful multi-modal AI model designed to generate high-quality novel videos using text, images, or video clips as input. By leveraging state-of-the-art deep learning techniques, it can synthesize realistic and visually impressive video content that can be used in a variety of applications, such as movie production, advertising, virtual reality, and more. 🎥\n\n## 🌟 Features\n\n- 📝 Generate videos from text descriptions\n- 🌃 Convert images into video sequences\n- 📼 Extend existing video clips with novel content\n- 🔮 High-quality output with customizable resolution\n- 🧠 Easy to use API for quick integration\n\n## 📦 Installation\n\nTo install Starlight Vision, simply use pip:\n\n```bash\npip install starlight-vision\n```\n\n## 🎬 Quick Start\n\nAfter we train you can install Starlight Vision and can start generating videos using the following code:\n\n```python\nimport torch\nfrom starlight_vision import Unet3D, ElucidatedStarlight, StarlightTrainer\n\nunet1 = Unet3D(dim = 64, dim_mults = (1, 2, 4, 8)).cuda()\n\nunet2 = Unet3D(dim = 64, dim_mults = (1, 2, 4, 8)).cuda()\n\n# elucidated starlight, which contains the unets above (base unet and super resoluting ones)\n\nstarlight = ElucidatedStarlight(\n    unets = (unet1, unet2),\n    image_sizes = (16, 32),\n    random_crop_sizes = (None, 16),\n    temporal_downsample_factor = (2, 1),        # in this example, the first unet would receive the video temporally downsampled by 2x\n    num_sample_steps = 10,\n    cond_drop_prob = 0.1,\n    sigma_min = 0.002,                          # min noise level\n    sigma_max = (80, 160),                      # max noise level, double the max noise level for upsampler\n    sigma_data = 0.5,                           # standard deviation of data distribution\n    rho = 7,                                    # controls the sampling schedule\n    P_mean = -1.2,                              # mean of log-normal distribution from which noise is drawn for training\n    P_std = 1.2,                                # standard deviation of log-normal distribution from which noise is drawn for training\n    S_churn = 80,                               # parameters for stochastic sampling - depends on dataset, Table 5 in apper\n    S_tmin = 0.05,\n    S_tmax = 50,\n    S_noise = 1.003,\n).cuda()\n\ntexts = [\n    'a whale breaching from afar',\n    'young girl blowing out candles on her birthday cake',\n    'fireworks with blue and green sparkles',\n    'dust motes swirling in the morning sunshine on the windowsill'\n]\n\nvideos = torch.randn(4, 3, 10, 32, 32).cuda() # (batch, channels, time / video frames, height, width)\n\n# feed images into starlight, training each unet in the cascade\n# for this example, only training unet 1\n\ntrainer = StarlightTrainer(starlight)\n\n# you can also ignore time when training on video initially, shown to improve results in video-ddpm paper. eventually will make the 3d unet trainable with either images or video. research shows it is essential (with current data regimes) to train first on text-to-image. probably won't be true in another decade. all big data becomes small data\n\ntrainer(videos, texts = texts, unet_number = 1, ignore_time = False)\ntrainer.update(unet_number = 1)\n\nvideos = trainer.sample(texts = texts, video_frames = 20) # extrapolating to 20 frames from training on 10 frames\n\nvideos.shape # (4, 3, 20, 32, 32)\n\n```\n\n## 🤝 Contributing\n\nWe welcome contributions from the community! If you'd like to contribute, please follow these steps:\n\n1. 🍴 Fork the repository on GitHub\n2. 🌱 Create a new branch for your feature or bugfix\n3. 📝 Commit your changes and push the branch to your fork\n4. 🚀 Create a pull request and describe your changes\n\n## 📄 License\n\nStarlight Vision is released under the APACHE License. See the [LICENSE](LICENSE) file for more details.\n\n## 🗺️ Roadmap\n\nThe following roadmap outlines our plans for future development and enhancements to Starlight Vision. We aim to achieve these milestones through a combination of research, development, and collaboration with the community.\n\n### 🚀 Short-term Goals\n\n- [ ] Improve text-to-video synthesis by incorporating advanced natural language understanding techniques\n- [ ] Train on LAION-5B and video datasets\n- [ ] Enhance the quality of generated videos through the implementation of state-of-the-art generative models\n- [ ] Optimize the model for real-time video generation on various devices, including mobile phones and edge devices\n- [ ] Develop a user-friendly web application that allows users to generate videos using Starlight Vision without any programming knowledge\n- [ ] Create comprehensive documentation and tutorials to help users get started with Starlight Vision\n\n### 🌌 Medium-term Goals\n\n- [ ] Integrate advanced style transfer techniques to allow users to customize the visual style of generated videos\n- [ ] Develop a plugin for popular video editing software (e.g., Adobe Premiere, Final Cut Pro) that enables users to utilize Starlight Vision within their existing workflows\n- [ ] Enhance the model's ability to generate videos with multiple scenes and complex narratives\n- [ ] Improve the model's understanding of object interactions and physics to generate more realistic videos\n- [ ] Expand the supported input formats to include audio, 3D models, and other media types\n\n### 🌠 Long-term Goals\n\n- [ ] Enable users to control the generated video with more granular parameters, such as lighting, camera angles, and object placement\n- [ ] Incorporate AI-driven video editing capabilities that automatically adjust the pacing, color grading, and transitions based on user preferences\n- [ ] Develop an API for real-time video generation that can be integrated into virtual reality, augmented reality, and gaming applications\n- [ ] Investigate methods for training Starlight Vision on custom datasets to generate domain-specific videos\n- [ ] Foster a community of researchers, developers, and artists to collaborate on the continued development and exploration of Starlight Vision's capabilities\n\n# Join Agora\nAgora is advancing Humanity with State of The Art AI Models like Starlight, join us and write your mark on the history books for eternity!\n\nhttps://discord.gg/sbYvXgqc\n\n\n\n## 🙌 Acknowledgments\n\nThis project is inspired by state-of-the-art research in video synthesis, such as the Structure and Content-Guided Video Synthesis with Diffusion Models paper, and leverages the power of deep learning frameworks like PyTorch.\n\nWe would like to thank the researchers, developers, and contributors who have made this project possible. 💫",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/StarlightVision',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
