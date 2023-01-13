import shlex

from os import PathLike
from typing import Union, List, Dict
from pathlib import Path
from IPython.display import display
from ipywidgets import widgets
from google.colab import drive, runtime

# fmt: off
#@title

#@markdown ### <font color="orange">***작업 디렉터리 경로***</font>
#@markdown 모델 파일 등이 영구적으로 보관될 디렉터리 경로
WORKSPACE = 'SD' #@param {type:"string"}

#@markdown ##### <font color="orange">***다운로드가 끝나면 자동으로 코랩 런타임을 종료할지?***</font>
DISCONNECT_RUNTIME = True  #@param {type:"boolean"}

# fmt: on

# 인터페이스 요소
dropdowns = widgets.VBox()
output = widgets.Output()
download_button = widgets.Button(
    description='다운로드',
    disabled=True,
    layout={"width": "99%"}
)

display(
    widgets.HBox(children=(
        widgets.VBox(
            children=(dropdowns, download_button),
            layout={"margin-right": "1em"}
        ),
        output
    )))


# 파일 경로
workspace_dir = Path('drive', 'MyDrive', WORKSPACE)
sd_model_dir = workspace_dir.joinpath('models', 'Stable-diffusion')
vae_dir = workspace_dir.joinpath('models', 'VAE')


class File:
    def __init__(self, url: str, path: PathLike, *extra_args: List[str]) -> None:
        self.url = url
        self.path = Path(path)
        self.extra_args = extra_args

    def download(self) -> None:
        output.clear_output()
        args = shlex.join((
            '--continue',
            '--always-resume',
            '--summary-interval', '3',
            '--console-log-level', 'error',
            '--max-concurrent-downloads', '16',
            '--max-connection-per-server', '16',
            '--split', '16',
            '--out', str(self.path.name),
            *self.extra_args,
            self.url
        ))

        with output:
            # aria2 로 파일 받아오기
            # fmt: off
            !which aria2c || apt install -y aria2
            output.clear_output()

            print('aria2 를 사용해 파일을 받아옵니다.')
            !aria2c {args}
            output.clear_output()

            print('파일을 성공적으로 받았습니다, 드라이브로 이동합니다.')
            print('이 작업은 파일의 크기에 따라 5분 이상 걸릴 수도 있으니 잠시만 기다려주세요.')
            if DISCONNECT_RUNTIME:
                print('작업이 완료되면 런타임을 자동으로 해제하니 다른 작업을 진행하셔도 좋습니다.')

            !rsync --remove-source-files -aP "{str(self.path.name)}" "{str(self.path)}"

            # fmt: on
            print('파일을 성공적으로 옮겼습니다, 이제 런타임을 해제해도 좋습니다.')


class ModelFile(File):
    def __init__(self, url: str, path: PathLike, **kwargs) -> None:
        if type(path) == str:
            path = sd_model_dir.joinpath(path)

        super().__init__(url, path, **kwargs)


class VaeFile(File):
    def __init__(self, url: str, path: PathLike, **kwargs) -> None:
        if type(path) == str:
            path = vae_dir.joinpath(path)

        super().__init__(url, path, **kwargs)


# 모델 목록
files = {
    'Stable-Diffusion Checkpoints': {
        'Stable Diffusion': {
            'v2.1': {
                '768-v': {
                    'ema-pruned': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.safetensors',
                            'stable-diffusion-v2-1-786-v-ema-pruned.safetensors'),
                        'ckpt': ModelFile(
                            'https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.ckpt',
                            'stable-diffusion-v2-1-786-v-ema-pruned.ckpt'),
                    },
                    'nonema-pruned': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-nonema-pruned.safetensors',
                            'stable-diffusion-v2-1-786-v-nonema-pruned.safetensors'),
                        'ckpt': ModelFile(
                            'https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-nonema-pruned.ckpt',
                            'stable-diffusion-v2-1-786-v-nonema-pruned.ckpt'),
                    }
                },
                '512-base': {
                    'ema-pruned': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/stabilityai/stable-diffusion-2-1-base/resolve/main/v2-1_512-ema-pruned.safetensors',
                            'stable-diffusion-v2-1-512-base-ema-pruned.safetensors'),
                        'ckpt': ModelFile(
                            'https://huggingface.co/stabilityai/stable-diffusion-2-1-base/resolve/main/v2-1_512-ema-pruned.ckpt',
                            'stable-diffusion-v2-1-512-base-ema-pruned.ckpt'),
                    },
                    'nonema-pruned': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/stabilityai/stable-diffusion-2-1-base/resolve/main/v2-1_512-nonema-pruned.safetensors',
                            'stable-diffusion-v2-1-512-base-nonema-pruned.safetensors'),
                        'ckpt': ModelFile(
                            'https://huggingface.co/stabilityai/stable-diffusion-2-1-base/resolve/main/v2-1_512-nonema-pruned.ckpt',
                            'stable-diffusion-v2-1-512-base-nonema-pruned.ckpt'),
                    },
                },
            },
            'v2.0': {
                '768-v-ema': {
                    'safetensors': ModelFile(
                        'https://huggingface.co/stabilityai/stable-diffusion-2/resolve/main/768-v-ema.safetensors',
                        'stable-diffusion-v2-0-786-v-ema.safetensors'),
                    'ckpt': ModelFile(
                        'https://huggingface.co/stabilityai/stable-diffusion-2/resolve/main/768-v-ema.ckpt',
                        'stable-diffusion-v2-0-786-v-ema.ckpt'),
                },
                '512-base-ema': {
                    'safetensors': ModelFile(
                        'https://huggingface.co/stabilityai/stable-diffusion-2-base/resolve/main/512-base-ema.safetensors',
                        'stable-diffusion-v2-0-512-base-ema.safetensors'),
                    'ckpt': ModelFile(
                        'https://huggingface.co/stabilityai/stable-diffusion-2-base/resolve/main/512-base-ema.ckpt',
                        'stable-diffusion-v2-0-512-base-ema.ckpt'),
                },
            },
            'v1.5': {
                'pruned-emaonly': {
                    'ckpt': ModelFile(
                        'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt',
                        'stable-diffusion-v1-5-pruned-emaonly.ckpt')
                },
                'pruned': {
                    'ckpt': ModelFile(
                        'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt',
                        'stable-diffusion-v1-5-pruned.ckpt')
                },
            },
        },

        'Waifu Diffusion': {
            'v1.4': {
                'anime_e1': {
                    'ckpt': [
                        ModelFile(
                            'https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/wd-1-4-anime_e1.ckpt',
                            'waifu-diffusion-v1-4-anime-e1.ckpt'),
                        ModelFile(
                            'https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/wd-1-4-anime_e1.yaml',
                            'waifu-diffusion-v1-4-anime-e1.yaml'),
                    ]
                },
                'booru-step-14000-unofficial': {
                    'safetensors': ModelFile(
                        'https://huggingface.co/waifu-diffusion/unofficial-releases/resolve/main/wd14-booru-step-14000-unofficial.safetensors',
                        'waifu-diffusion-v1-4-booru-step-14000.ckpt'),
                },
            },
            'v1.3.5': {
                '80000-fp32': {
                    'ckpt': ModelFile(
                        'https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/models/wd-1-3-5_80000-fp32.ckpt',
                        'waifu-diffusion-v1-4-80000-fp32.ckpt'),
                },
                'penultimate-ucg-cont': {
                    'ckpt': ModelFile(
                        'https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/models/wd-1-3-penultimate-ucg-cont.ckpt',
                        'waifu-diffusion-v1-3-5-penultimate-ucg-cont.ckpt'),
                }
            },
            'v1.3': {
                'fp16': {
                    'ckpt': ModelFile(
                        'https://huggingface.co/hakurei/waifu-diffusion-v1-3/resolve/main/wd-v1-3-float16.ckpt',
                        'waifu-diffusion-v1-3-float16.ckpt')
                },
                'fp32': {
                    'ckpt': ModelFile(
                        'https://huggingface.co/hakurei/waifu-diffusion-v1-3/resolve/main/wd-v1-3-float32.ckpt',
                        'waifu-diffusion-v1-3-float32.ckpt')
                },
                'full': {
                    'ckpt': ModelFile(
                        'https://huggingface.co/hakurei/waifu-diffusion-v1-3/resolve/main/wd-v1-3-full.ckpt',
                        'waifu-diffusion-v1-3-full.ckpt')
                },
                'full-opt': {
                    'ckpt': ModelFile(
                        'https://huggingface.co/hakurei/waifu-diffusion-v1-3/resolve/main/wd-v1-3-full-opt.ckpt',
                        'waifu-diffusion-v1-3-full-opt.ckpt')
                },
            },
        },

        'OrangeMixs': {
            'AbyssOrangeMix': {
                '2': {
                    'hard': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix2/AbyssOrangeMix2_hard.safetensors',
                            'AbyssOrangeMix2_hard.safetensors'),
                    },
                    'nsfw': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix2/AbyssOrangeMix2_nsfw.safetensors',
                            'AbyssOrangeMix2_nsfw.safetensors'),
                    },
                    'sfw': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix2/AbyssOrangeMix2_sfw.safetensors',
                            'AbyssOrangeMix2_sfw.safetensors'),
                        'ckpt': ModelFile(
                            'https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix2/AbyssOrangeMix2_sfw.ckpt',
                            'AbyssOrangeMix2_sfw.ckpt')
                    }
                },
                '1': {
                    'half': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix/AbyssOrangeMix_half.safetensors',
                            'AbyssOrangeMix_half.safetensors'),
                    },
                    'night': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix/AbyssOrangeMix_Night.safetensors',
                            'AbyssOrangeMix_night.safetensors'),
                    },
                    'base': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix/AbyssOrangeMix.safetensors',
                            'AbyssOrangeMix_base.safetensors'),
                        'ckpt': ModelFile(
                            'https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix/AbyssOrangeMix_base.ckpt',
                            'AbyssOrangeMix_base.ckpt'),
                    },
                }
            }
        },

        'Anything': {
            'v3.0': {
                'better-vae': {
                    'fp32': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/Linaqruf/anything-v3-better-vae/resolve/main/any-v3-fp32-better-vae.safetensors',
                            'anything-v3-0-fp32-better-vae.safetensors'),
                        'ckpt': ModelFile(
                            'https://huggingface.co/Linaqruf/anything-v3-better-vae/resolve/main/any-v3-fp32-better-vae.ckpt',
                            'anything-v3-0-fp32-better-vae.ckpt'),
                    }
                },
                'pruned': {
                    'fp16': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0-pruned-fp16.safetensors',
                            'anything-v3-0-pruned-fp16.safetensors'),
                        'ckpt': ModelFile(
                            'https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0-pruned-fp16.ckpt',
                            'anything-v3-0-pruned-fp16.ckpt'),
                    },
                    'fp32': {
                        'safetensors': ModelFile(
                            'https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0-pruned-fp32.safetensors',
                            'anything-v3-0-pruned-fp32.safetensors'),
                        'ckpt': ModelFile(
                            'https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0-pruned-fp32.ckpt',
                            'anything-v3-0-pruned-fp32.ckpt')
                    },
                    'safetensors': ModelFile(
                        'https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0-pruned.safetensors',
                        'anything-v3-0-pruned.safetensors'),
                    'ckpt': ModelFile(
                        'https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0-pruned.ckpt',
                        'anything-v3-0-pruned.ckpt'),
                },
                'safetensors': ModelFile(
                    'https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0.safetensors',
                    'anything-v3-0.safetensors'),
                'ckpt': ModelFile(
                    'https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0.ckpt',
                    'anything-v3-0.ckpt'),
            }
        },
    },
    'VAEs': {
        'Stable Diffusion': {
            'vae-ft-mse-840000': {
                'pruned': {
                    'safetensors': VaeFile(
                        'https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors',
                        'stable-diffusion-vae-ft-mse-840000-ema-pruned.safetensors'),
                    'ckpt': VaeFile(
                        'https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.ckpt',
                        'stable-diffusion-vae-ft-mse-840000-ema-pruned.ckpt')
                }
            },
            'vae-ft-ema-560000': {
                'safetensors': VaeFile(
                    'https://huggingface.co/stabilityai/sd-vae-ft-ema-original/resolve/main/vae-ft-ema-560000-ema-pruned.safetensors',
                    'stable-diffusion-vae-ft-ema-560000-ema-pruned.safetensors'),
                'ckpt': VaeFile(
                    'https://huggingface.co/stabilityai/sd-vae-ft-ema-original/resolve/main/vae-ft-ema-560000-ema-pruned.ckpt',
                    'stable-diffusion-vae-ft-ema-560000-ema-pruned.ckpt'),
            }
        },

        'NovelAI': {
            'animevae.pt': VaeFile(
                'https://huggingface.co/gozogo123/anime-vae/resolve/main/animevae.pt',
                'novelai-animevae.pt')
        }
    }
}

with output:
    # 구글 드라이브 마운팅
    drive.mount('drive')


def global_disable(disabled: bool):
    for dropdown in dropdowns.children:
        dropdown.disabled = disabled

    download_button.disabled = disabled

    # 마지막 드롭다운이 하위 드롭다운이라면 버튼 비활성화하기
    if not disabled:
        dropdown = dropdowns.children[len(dropdowns.children) - 1]
        download_button.disabled = isinstance(dropdown, dict)


def on_download(_):
    dropdown = dropdowns.children[len(dropdowns.children) - 1]
    entry = dropdown.entries[dropdown.value]

    global_disable(True)

    # 단일 파일 받기
    if isinstance(entry, File):
        entry.download()

    # 다중 파일 받기
    elif isinstance(entry, list):
        for file in entry:
            file.download()

    # TODO: 오류 처리
    else:
        pass

    if DISCONNECT_RUNTIME:
        runtime.unassign()

    global_disable(False)


def on_dropdown_change(event):
    dropdown: widgets.Dropdown = event['owner']
    entries: Union[List, Dict] = dropdown.entries[event['new']]

    # 이전 하위 드롭다운 전부 제거하기
    dropdowns.children = dropdowns.children[:dropdown.children_index + 1]

    if isinstance(entries, dict):
        download_button.disabled = True
        create_dropdown(entries)
        return

    # 하위 드롭다운 만들기
    download_button.disabled = False


def create_dropdown(entries: Dict) -> widgets.Dropdown:
    options = list(entries.keys())
    value = options[0]
    dropdown = widgets.Dropdown(
        options=options,
        value=value)

    setattr(dropdown, 'children_index', len(dropdowns.children))
    setattr(dropdown, 'entries', entries)

    dropdowns.children = tuple(list(dropdowns.children) + [dropdown])

    dropdown.observe(on_dropdown_change, names='value')

    on_dropdown_change({
        'owner': dropdown,
        'new': value
    })

    return dropdown


# 첫 엔트리 드롭다운 만들기
create_dropdown(files)

download_button.on_click(on_download)
