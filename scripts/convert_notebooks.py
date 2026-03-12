#!/usr/bin/env python3
"""Convert Jupyter notebooks to markdown with Colab buttons."""

import subprocess
import shutil
import os
from pathlib import Path

STUDY_ROOT = Path("/home/weed/study")
SITE_ROOT = Path("/home/weed/study/study-site")
DOCS_ROOT = SITE_ROOT / "docs"
ASSETS_ROOT = SITE_ROOT / "assets" / "images"
NOTEBOOKS_ROOT = SITE_ROOT / "notebooks"

# GitHub repo placeholder - update after repo creation
GITHUB_OWNER = "OWNER"
GITHUB_REPO = "study-site"
GITHUB_BRANCH = "main"

COLAB_BADGE = "https://colab.research.google.com/assets/colab-badge.svg"

# AI notebook -> topic page mapping
AI_TOPICS = {
    "python-basics": {
        "title": "Python 기초",
        "notebooks": ["basic/강의_3기_AI개론_1차시__python_.ipynb"],
    },
    "eda": {
        "title": "EDA (탐색적 데이터 분석)",
        "notebooks": ["basic/강의_3기_AI개론_2차시__EDA_.ipynb"],
    },
    "pytorch-intro": {
        "title": "PyTorch 입문",
        "notebooks": ["basic/강의_3기_AI개론_3차시__pytorch_.ipynb"],
    },
    "neural-network-fundamentals": {
        "title": "신경망 기초",
        "notebooks": [
            "basic/강의_3기_AI개론_4차시__Perceptron_BP_ActivationF_.ipynb",
            "basic/강의_3기_AI개론_5차시__GD_.ipynb",
            "basic/강의_3기_AI개론_6차시__Object_function_.ipynb",
        ],
    },
    "deep-learning": {
        "title": "딥러닝 (분류/회귀)",
        "notebooks": [
            "basic/강의_3기_AI개론_7차시__Regression_.ipynb",
            "basic/강의_3기_AI개론_8차시__Binary_.ipynb",
            "basic/강의_3기_AI개론_9차시__Multinomial_.ipynb",
            "basic/강의_3기_AI개론_10차시__MNIST_.ipynb",
        ],
    },
    "cnn-architectures": {
        "title": "CNN 아키텍처",
        "notebooks": [
            "basic/강의_3기_AI개론_11차시__CNN_.ipynb",
            "basic/강의_3기_AI개론_12차시__SGD_Adam_.ipynb",
            "basic/강의_3기_AI개론_13차시__AlexNet_GoogleNet_.ipynb",
            "basic/강의_3기_AI개론_14차시__VGG_ResNet_.ipynb",
        ],
    },
    "object-detection": {
        "title": "객체 탐지",
        "notebooks": [
            "basic/강의_3기_AI개론_15차시__Transfer_learning_.ipynb",
            "basic/강의_3기_AI개론_16차시__model_from_scratch_.ipynb",
            "basic/강의_3기_AI개론_17차시__FasterRCNN_MaskedRCNN_.ipynb",
            "basic/강의_3기_AI개론_18차시__SSD_Yolo_.ipynb",
        ],
    },
    "sequence-models": {
        "title": "시퀀스 모델 (RNN/LSTM)",
        "notebooks": [
            "basic/강의_3기_AI개론_19차시__RNN_LSTM_.ipynb",
            "intermediate/강의_3기_AI응용_6차시__DeepRNN_.ipynb",
        ],
    },
    "vision-transformers": {
        "title": "Vision Transformer",
        "notebooks": ["basic/강의_3기_AI개론_20차시__ViT_.ipynb"],
    },
    "computer-vision": {
        "title": "컴퓨터비전 (OpenCV)",
        "notebooks": [
            "intermediate/강의_3기_AI응용_1차시__OpenCV1_.ipynb",
            "intermediate/강의_3기_AI응용_2차시__OpenCV2_.ipynb",
            "intermediate/강의_3기_AI응용_3차시__OpenCV3_.ipynb",
        ],
    },
    "advanced-cv": {
        "title": "고급 CV (Tracking/Detection)",
        "notebooks": [
            "intermediate/강의_3기_AI응용_4차시__object_tracking_.ipynb",
            "intermediate/강의_3기_AI응용_4차시__RAFT_.ipynb",
            "intermediate/강의_3기_AI응용_5차시__DeepCNN_trash_detection_.ipynb",
        ],
    },
    "generative-models": {
        "title": "생성 모델 (GAN/NeRF)",
        "notebooks": [
            "intermediate/강의_3기_AI응용_7차시__style_transfer_.ipynb",
            "intermediate/강의_3기_AI응용_8차시__GAN_.ipynb",
            "intermediate/강의_3기_AI응용_9차시__NeRF_.ipynb",
        ],
    },
    "explainable-ai": {
        "title": "Explainable AI",
        "notebooks": ["intermediate/강의_3기_AI응용_10차시__Explainable_AI_.ipynb"],
    },
    "medical-ai": {
        "title": "의료 AI",
        "notebooks": ["intermediate/강의_3기_AI응용_11차시__Pneumonia__colab.ipynb"],
    },
    "reinforcement-learning": {
        "title": "강화학습",
        "notebooks": [
            "intermediate/강의_3기_AI응용_12차시__RL1_.ipynb",
            "intermediate/강의_3기_AI응용_13차시__RL2_MC_.ipynb",
            "intermediate/강의_3기_AI응용_13차시__RL2_Q_.ipynb",
            "intermediate/강의_3기_AI응용_14차시__DQN_.ipynb",
        ],
    },
}

# ROS notebook -> lesson mapping (notebooks that belong to lesson pages)
ROS_NOTEBOOKS = {
    "ros/intro/lesson-02": [
        "jupyter_ros/py_pubsub.ipynb",
        "jupyter_ros/PublisherTest.ipynb",
        "jupyter_ros/SubscriptionTest.ipynb",
    ],
    "ros/intro/lesson-03": ["jupyter_ros/triangle_turtle.ipynb"],
    "ros/intro/lesson-04": ["jupyter_ros/ros2_function.ipynb"],
    "ros/intro/lesson-05": ["jupyter_ros/ServiceClientTest.ipynb"],
    "ros/intro/lesson-07": [
        "7차시_수업코드_개선_/7차시 수업코드(개선)/7차시_예제_주피터노트북_py_pubsub.ipynb",
        "7차시_수업코드_개선_/7차시 수업코드(개선)/7차시_주피터완성본_py_srvcli.ipynb",
    ],
    "ros/intro/lesson-08": [
        "jupyter_ros/8차시_1_temperature_example.ipynb",
        "jupyter_ros/8차시_2_my_robot_system_설명.ipynb",
    ],
    "ros/intro/lesson-09": [
        "jupyter_ros/9차시_1_ROS2_API함수정리.ipynb",
        "jupyter_ros/9차시_2_주피터노트북_사용시_주의사항.ipynb",
        "jupyter_ros/9차시_3_cam_실행.ipynb",
        "jupyter_ros/9차시_4_hangman_api_list.ipynb",
    ],
}


def get_colab_url(notebook_rel_path: str) -> str:
    """Generate Colab URL for a notebook."""
    return (
        f"https://colab.research.google.com/github/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/"
        f"notebooks/{notebook_rel_path}"
    )


def convert_notebook_to_md(nb_path: Path, img_output_dir: Path) -> str:
    """Convert a single notebook to markdown string."""
    img_output_dir.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            [
                "jupyter", "nbconvert",
                "--to", "markdown",
                "--output-dir", str(img_output_dir),
                str(nb_path),
            ],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            return f"> Notebook conversion failed: {result.stderr[:200]}\n"

        # Read the generated markdown
        md_name = nb_path.stem + ".md"
        md_path = img_output_dir / md_name
        if md_path.exists():
            content = md_path.read_text(encoding="utf-8")
            md_path.unlink()  # Remove temp md, we'll embed content
            return content
        return "> Notebook conversion produced no output.\n"
    except Exception as e:
        return f"> Notebook conversion error: {e}\n"


def copy_notebook(nb_rel_path: str, source_base: Path):
    """Copy notebook to site's notebooks/ directory for Colab links."""
    src = source_base / nb_rel_path
    if not src.exists():
        print(f"  [WARNING] Notebook not found: {src}")
        return

    # Determine destination
    dst = NOTEBOOKS_ROOT / nb_rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def process_ai_topics():
    """Process all AI topic pages."""
    print("\n=== Processing AI Topics ===\n")
    ai_root = STUDY_ROOT / "Rokey-AI"
    ai_docs = DOCS_ROOT / "ai"
    ai_docs.mkdir(parents=True, exist_ok=True)

    for topic_key, topic_info in AI_TOPICS.items():
        print(f"Topic: {topic_info['title']}")
        md_lines = [f"# {topic_info['title']}\n"]

        for nb_rel in topic_info["notebooks"]:
            nb_path = ai_root / nb_rel
            nb_name = nb_path.stem

            # Colab button
            colab_nb_path = nb_rel
            colab_url = get_colab_url(colab_nb_path)
            md_lines.append(
                f"\n## {nb_name}\n\n"
                f"[![Open In Colab]({COLAB_BADGE})]({colab_url})\n"
            )

            # Convert notebook
            img_dir = ASSETS_ROOT / "ai" / topic_key
            content = convert_notebook_to_md(nb_path, img_dir)

            # Fix image paths in content
            # nbconvert outputs images as {stem}_files/...
            files_dir_name = f"{nb_path.stem}_files"
            rel_img_path = f"../../assets/images/ai/{topic_key}/{files_dir_name}"
            content = content.replace(f"![png]({files_dir_name}/", f"![png]({rel_img_path}/")
            content = content.replace(f"![jpeg]({files_dir_name}/", f"![jpeg]({rel_img_path}/")
            content = content.replace(f"![svg]({files_dir_name}/", f"![svg]({rel_img_path}/")

            md_lines.append(content)

            # Copy notebook for Colab
            copy_notebook(nb_rel, ai_root)

        # Write topic page
        md_path = ai_docs / f"{topic_key}.md"
        md_path.write_text("\n".join(md_lines), encoding="utf-8")
        print(f"  -> {md_path.name}")


def process_ros_notebooks():
    """Append notebook content to existing ROS lesson pages."""
    print("\n=== Processing ROS Notebooks ===\n")
    ros_root = STUDY_ROOT / "ROS-study"

    for lesson_path, nb_list in ROS_NOTEBOOKS.items():
        md_path = DOCS_ROOT / f"{lesson_path}.md"
        if not md_path.exists():
            print(f"  [WARNING] Lesson page not found: {md_path}")
            continue

        print(f"Lesson: {lesson_path}")
        existing = md_path.read_text(encoding="utf-8")
        md_lines = [existing, "\n---\n\n## Jupyter Notebooks\n"]

        section = "/".join(lesson_path.split("/")[:2])
        page_name = lesson_path.split("/")[-1]

        for nb_rel in nb_list:
            nb_path = ros_root / nb_rel
            nb_name = nb_path.stem

            # Colab button
            colab_nb_path = f"ros/{nb_rel}"
            colab_url = get_colab_url(colab_nb_path)
            md_lines.append(
                f"\n### {nb_name}\n\n"
                f"[![Open In Colab]({COLAB_BADGE})]({colab_url})\n"
            )

            # Convert notebook
            img_dir = ASSETS_ROOT / section / page_name
            content = convert_notebook_to_md(nb_path, img_dir)

            # Fix image paths
            files_dir_name = f"{nb_path.stem}_files"
            rel_img_path = f"../../assets/images/{section}/{page_name}/{files_dir_name}"
            content = content.replace(f"![png]({files_dir_name}/", f"![png]({rel_img_path}/")
            content = content.replace(f"![jpeg]({files_dir_name}/", f"![jpeg]({rel_img_path}/")

            md_lines.append(content)

            # Copy notebook for Colab
            dst_dir = NOTEBOOKS_ROOT / "ros" / Path(nb_rel).parent
            dst_dir.mkdir(parents=True, exist_ok=True)
            if nb_path.exists():
                shutil.copy2(nb_path, dst_dir / nb_path.name)

        md_path.write_text("\n".join(md_lines), encoding="utf-8")
        print(f"  -> updated {md_path.name}")


def main():
    print("=== Notebook Conversion Pipeline ===")
    process_ai_topics()
    process_ros_notebooks()
    print("\n=== Done ===")


if __name__ == "__main__":
    main()
