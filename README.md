# Drill13 — 아이템 선택 게임

Pico2D와 게임 프레임워크를 이용한 소년 게임입니다. 로고 화면이 끝나면 제목
화면이 나타나고, Space를 누르면 게임을 시작합니다.

## 실행

이 폴더에서 PowerShell을 열어 다음을 실행합니다.

```powershell
python -m pip install -r LEC15_Game_Framework/requirements.txt
python LEC15_Game_Framework/main.py
```

VS Code에서는 `LEC15_Game_Framework/main.py`를 실행해도 됩니다. 다른 Python
인터프리터를 사용한다면 해당 인터프리터에도 `pico2d`와 `transitions`가
설치되어 있어야 합니다.

## 조작

- **왼쪽·오른쪽 방향키**: 소년 이동
- **Space**: 바라보는 방향으로 선택한 공 발사. SLEEP에서는 소년을 깨움
- **I**: 게임을 멈추고 아이템 선택 화면 열기
- 아이템 화면에서 **1**: 21×21 공 선택 후 게임으로 돌아가기
- 아이템 화면에서 **2**: 41×41 공 선택 후 게임으로 돌아가기
- 아이템 화면에서 **0**: 공 발사 중지 후 게임으로 돌아가기
- 아이템 화면에서 **I 또는 Esc**: 기존 선택을 유지하고 돌아가기
- 게임 중 **P**: 일시정지 화면 열기. 일시정지 화면에서 다시 P를 눌러 복귀
- 게임 중 **Esc**: 제목 화면으로 이동

처음 시작하면 21×21 공이 선택됩니다. 0을 선택해도 이미 발사된 공은 계속
이동합니다. 선택은 현재 게임을 플레이하는 동안 유지되며, 게임을 다시
시작하면 기본 공으로 돌아갑니다.

## 검증

```powershell
python -m unittest discover -s LEC15_Game_Framework/tests -v
```

아이템 모드 요구사항과 상태 전환은 [PRD.md](PRD.md)를 참고하세요.
