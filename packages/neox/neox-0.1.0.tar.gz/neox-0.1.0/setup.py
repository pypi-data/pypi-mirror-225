# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neox']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'transformers']

setup_kwargs = {
    'name': 'neox',
    'version': '0.1.0',
    'description': 'An Multi-Modality Foundation Model for Humanoid robots',
    'long_description': '# NeoCortex: Multi-Modality Foundation Model for Humanoid Robots\n\nNeoCortex is a cutting-edge, multi-modality foundation model engineered for humanoid robots. With the capability to process an array of modalities including images, text, videos, depth, heatmaps, LIDAR, 3D scenes, point clouds, and more, NeoCortex represents the zenith of robotic perception and cognition.\n\n## Installation\nTo integrate NeoCortex into your development environment:\n\n```bash\npip install neocortex\n```\n\n## Usage\n```python\nimport torch\nfrom neocortex import NeoCortex\n\n# Sample usage\ndata = {\n    \'image\': torch.randn(1, 3, 256, 256),\n    \'text\': "sample text input",\n    \'lidar\': torch.randn(1, 512, 512)\n}\n\nmodel = NeoCortex()\noutput = model(data)\n```\n\n## Model Architecture\nBuilding on the paradigms established by models like NeVA, NeoCortex expands its horizons to embrace a multi-faceted input system:\n\n- **Images**: Processed through a frozen variant of the Hugging Face CLIP model, producing image embeddings.\n- **Text**: Integrated seamlessly with an NVIDIA-trained GPT variant.\n- **LIDAR**: Point clouds processed through PointNet or KPConv, extracting essential spatial features. These features, once captured, are projected to text embedding dimensions.\n- **Videos**: Processed using 3D-CNNs to capture temporal information, then integrated with the main architecture.\n- **Heatmaps, 3D Scenes, and Depth**: These are funneled through specialized modules tailored for each modality before being integrated.\n\nTraining comprises three stages:\n1. **Pretraining**: Specific modules (like PointNet for LIDAR) are pretrained, with the main model frozen.\n2. **Inter-modality Training**: The embeddings from different modalities are concatenated, projected, and trained to ensure inter-modality coherence.\n3. **Finetuning**: Utilizing synthetic data generated with advanced GPT versions to ensure the model understands the intricate relationship between various modalities.\n\n## Specifications\n\n- **Architecture Type**: Multi-Modality Transformer\n- **Sub-Architectures**: GPT, CLIP, PointNet, 3D-CNN\n- **Model versions**: 10B, 30B, 50B\n\n## Input & Output\n\n- **Input Formats**: \n  - Images: RGB\n  - Text: Tokens\n  - LIDAR: Point Clouds\n  - Videos: Frames\n  - And more...\n- **Output Format**: Text or Action Tokens\n\n## Integration and Compatibility\n\n- **Supported Hardware Platforms**: Hopper, Ampere/Turing, specialized robotic chipsets\n- **Supported Operating Systems**: Linux, RoboOS\n\n## Training & Fine-tuning Data\n\n- **Image Dataset**: [Link to Dataset]\n- **LIDAR Dataset**: [Link to Dataset]\n- **Textual Data**: Synthetically produced by GPT versions\n- **Licenses**: Various, mainly MIT and CC-BY-NC 4.0\n\n## Inference\n\n- **Engine**: Triton and specialized robotic inference engines\n- **Test Hardware**: Humanoid robotic platforms\n\n## References and More\n\n- [Visual Instruction Tuning paper](#)\n- [Blog](#)\n- [Codebase](https://github.com/kyegomez/NeoCortex)\n- [Demo](#)\n\n## Licensing\nThis project is licensed under the MIT License.\n\nFor more details, contributions, and support, please refer to the [official repository](https://github.com/kyegomez/NeoCortex).',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/NeoCortex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
