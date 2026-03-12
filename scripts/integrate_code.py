#!/usr/bin/env python3
"""Integrate ROS2 code into lesson pages and generate code-ref pages."""

from pathlib import Path

STUDY_ROOT = Path("/home/weed/study")
SITE_ROOT = Path("/home/weed/study/study-site")
DOCS_ROOT = SITE_ROOT / "docs"
ROS_STUDY = STUDY_ROOT / "ROS-study"

GITHUB_OWNER = "OWNER"
GITHUB_REPO = "study-site"
GITHUB_BRANCH = "main"

MAX_CODE_LINES = 50  # Show first N lines in code blocks

# Code directories -> lesson page mapping
LESSON_CODE = {
    "ros/intro/lesson-02": ["turtlesim/my_first_package/"],
    "ros/intro/lesson-03": ["turtlesim/tultle_move/"],
    "ros/intro/lesson-04": ["py_pubsub_qos/"],
    "ros/intro/lesson-05": ["py_srvcli/"],
    "ros/intro/lesson-06": ["ros2env/"],
    "ros/intro/lesson-07": ["7차시_수업코드_개선_/"],
    "ros/intro/lesson-08": ["calculator_project_py/", "my_robot_/"],
    "ros/intro/lesson-09": ["hangman_game/", "hangman_interfaces/", "my_cam_pubsub/"],
}

# Code-ref pages: standalone code reference pages
CODE_REF_PAGES = {
    "turtlesim": {
        "title": "Turtlesim",
        "description": "ROS2 Turtlesim 기반 프로젝트 모음 (pub/sub, 브라운 운동, 터틀 이동 등)",
        "dirs": ["turtlesim/"],
    },
    "pubsub-qos": {
        "title": "Pub/Sub & QoS",
        "description": "Publisher/Subscriber with Quality of Service settings",
        "dirs": ["py_pubsub_qos/"],
    },
    "srvcli": {
        "title": "Service/Client",
        "description": "ROS2 Service와 Client 구현 예제",
        "dirs": ["py_srvcli/"],
    },
    "calculator": {
        "title": "Calculator",
        "description": "ROS2 패키지로 구현한 산술 연산 계산기 프로젝트",
        "dirs": ["calculator_project_py/"],
    },
    "robot-system": {
        "title": "Robot System",
        "description": "센서 노드, 쿨러 서비스, 액션 서버를 포함한 로봇 시스템 제어",
        "dirs": ["my_robot_/"],
    },
    "camera": {
        "title": "Camera Pub/Sub",
        "description": "카메라 이미지 Publisher/Subscriber 노드",
        "dirs": ["my_cam_pubsub/"],
    },
    "hangman": {
        "title": "Hangman Game",
        "description": "ROS2 Action을 활용한 행맨 게임",
        "dirs": ["hangman_game/", "hangman_interfaces/"],
    },
    "urdf": {
        "title": "URDF & Xacro",
        "description": "로봇 모델 기술을 위한 URDF와 Xacro 파일",
        "dirs": ["my_urdf/", "urdf_revolution/"],
    },
    "opencv": {
        "title": "OpenCV (Hough Transform)",
        "description": "OpenCV를 활용한 Hough 변환 예제",
        "dirs": ["opencv/"],
    },
    "point-cloud": {
        "title": "Point Cloud",
        "description": "PCD 파일 기반 포인트 클라우드 처리",
        "dirs": ["point_cloud/"],
    },
    "lane-detect": {
        "title": "Lane Detection",
        "description": "슬라이딩 윈도우 알고리즘을 활용한 차선 검출",
        "dirs": ["lane_detect/"],
    },
    "qt-plugin": {
        "title": "Qt Plugin (C++)",
        "description": "C++ Qt GUI 플러그인 프로젝트",
        "dirs": ["cpp_qt_plugin/"],
    },
    "rqt": {
        "title": "RQT Example",
        "description": "RQT GUI 플러그인 예제",
        "dirs": ["rqt_example/"],
    },
    "ros2env": {
        "title": "ROS2 환경설정",
        "description": "ROS2 환경 설정 도구",
        "dirs": ["ros2env/"],
    },
}

CODE_EXTENSIONS = {".py", ".cpp", ".h", ".hpp", ".xml", ".yaml", ".yml",
                   ".launch.py", ".xacro", ".urdf", ".msg", ".srv", ".action"}


def get_github_url(rel_path: str) -> str:
    """Generate GitHub URL for a file or directory."""
    return f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/tree/{GITHUB_BRANCH}/source/{rel_path}"


def find_code_files(base_dir: Path) -> list[Path]:
    """Find all code files in a directory, sorted by importance."""
    files = []
    for ext in CODE_EXTENSIONS:
        files.extend(base_dir.rglob(f"*{ext}"))

    # Filter out test files and __pycache__
    files = [f for f in files if "__pycache__" not in str(f)
             and "test_" not in f.name
             and ".egg-info" not in str(f)]

    # Sort: .py first, then .cpp, then others; main files first
    def sort_key(f):
        priority = 10
        name = f.name.lower()
        if "main" in name or "node" in name or "launch" in name:
            priority = 0
        elif f.suffix == ".py":
            priority = 1
        elif f.suffix in (".cpp", ".h"):
            priority = 2
        elif f.suffix in (".msg", ".srv", ".action"):
            priority = 3
        return (priority, f.name)

    return sorted(files, key=sort_key)


def format_code_block(file_path: Path, base_dir: Path) -> str:
    """Format a code file as a markdown code block with truncation."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

    lines = content.split("\n")
    rel_path = file_path.relative_to(base_dir)
    lang = {
        ".py": "python", ".cpp": "cpp", ".h": "cpp", ".hpp": "cpp",
        ".xml": "xml", ".yaml": "yaml", ".yml": "yaml",
        ".xacro": "xml", ".urdf": "xml",
        ".msg": "text", ".srv": "text", ".action": "text",
    }.get(file_path.suffix, "text")

    # For launch.py files
    if file_path.name.endswith(".launch.py"):
        lang = "python"

    truncated = len(lines) > MAX_CODE_LINES
    display_lines = lines[:MAX_CODE_LINES]

    md = f"#### `{rel_path}`\n\n"
    md += f"```{lang}\n"
    md += "\n".join(display_lines)
    if truncated:
        md += f"\n# ... ({len(lines) - MAX_CODE_LINES} more lines)"
    md += "\n```\n"

    return md


def generate_code_ref_page(page_key: str, page_info: dict) -> str:
    """Generate a code reference page."""
    md_lines = [
        f"# {page_info['title']}\n",
        f"{page_info['description']}\n",
    ]

    for dir_rel in page_info["dirs"]:
        dir_path = ROS_STUDY / dir_rel
        if not dir_path.exists():
            md_lines.append(f"\n> Directory `{dir_rel}` not found.\n")
            continue

        github_url = get_github_url(dir_rel)
        md_lines.append(f"\n[View full source on GitHub]({github_url}){{ .md-button }}\n")

        code_files = find_code_files(dir_path)
        if not code_files:
            md_lines.append("> No code files found.\n")
            continue

        # Show top 5 most important files
        for f in code_files[:5]:
            block = format_code_block(f, ROS_STUDY)
            if block:
                md_lines.append(block)

        remaining = len(code_files) - 5
        if remaining > 0:
            md_lines.append(
                f"\n*... and {remaining} more files. "
                f"[See full source on GitHub]({github_url})*\n"
            )

    return "\n".join(md_lines)


def append_code_to_lessons():
    """Append code snippets to existing lesson pages."""
    print("\n=== Appending Code to Lesson Pages ===\n")

    for lesson_path, dirs in LESSON_CODE.items():
        md_path = DOCS_ROOT / f"{lesson_path}.md"
        if not md_path.exists():
            print(f"  [SKIP] {md_path} not found")
            continue

        existing = md_path.read_text(encoding="utf-8")
        md_lines = [existing, "\n---\n\n## Code Examples\n"]

        for dir_rel in dirs:
            dir_path = ROS_STUDY / dir_rel
            if not dir_path.exists():
                continue

            github_url = get_github_url(dir_rel)
            md_lines.append(f"\n### `{dir_rel}`\n")
            md_lines.append(f"[View full source on GitHub]({github_url}){{ .md-button }}\n")

            code_files = find_code_files(dir_path)
            for f in code_files[:3]:  # Top 3 per directory in lessons
                block = format_code_block(f, ROS_STUDY)
                if block:
                    md_lines.append(block)

        md_path.write_text("\n".join(md_lines), encoding="utf-8")
        print(f"  -> updated {lesson_path}")


def generate_all_code_ref_pages():
    """Generate all code reference pages."""
    print("\n=== Generating Code Reference Pages ===\n")

    code_ref_dir = DOCS_ROOT / "ros" / "code-ref"
    code_ref_dir.mkdir(parents=True, exist_ok=True)

    for page_key, page_info in CODE_REF_PAGES.items():
        content = generate_code_ref_page(page_key, page_info)
        md_path = code_ref_dir / f"{page_key}.md"
        md_path.write_text(content, encoding="utf-8")
        print(f"  -> {page_key}.md")


def copy_source_files():
    """Copy source code to site's source/ directory for GitHub links."""
    print("\n=== Copying Source Files ===\n")
    source_dir = SITE_ROOT / "source"

    all_dirs = set()
    for page_info in CODE_REF_PAGES.values():
        all_dirs.update(page_info["dirs"])
    for dirs in LESSON_CODE.values():
        all_dirs.update(dirs)

    import shutil
    for dir_rel in sorted(all_dirs):
        src = ROS_STUDY / dir_rel
        if src.exists():
            dst = source_dir / dir_rel
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(
                src, dst,
                symlinks=False,
                ignore=shutil.ignore_patterns(
                    "__pycache__", "*.egg-info", ".git", "*.pyc",
                    "log", "build", "install",
                ),
                ignore_dangling_symlinks=True,
            )
            print(f"  -> {dir_rel}")


def main():
    print("=== Code Integration Pipeline ===")
    generate_all_code_ref_pages()
    append_code_to_lessons()
    copy_source_files()
    print("\n=== Done ===")


if __name__ == "__main__":
    main()
