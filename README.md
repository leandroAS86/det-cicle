# DetCicle:: Detecção de Ciclistas :bike:

## Este projeto foi desenvolvido como tema de pesquisa de mestrado no [Programa de Pós Graduação em Computação Aplicada - PPGCA](https://www.utfpr.edu.br/cursos/coordenacoes/stricto-sensu/ppgca-ct) da [Universidade Tecnologica Federal do Paraná - UTFPR](https://www.utfpr.edu.br/).

## Proposta :dart:
DetCicle é um sistema embarcado para contagem automática de ciclistas em cenários urbanos, em tempo real, por meio da captura de imagens com câmeras de vídeo. A contagem é realizada por meio de visão computacional e do modelo YOLOv8 de aprendizagem profunda.

### Resumo 
A detecção automática de ciclistas no cenário urbano é um campo de estudo em sistemas de transporte inteligentes e smart cities que possibilita gerar dados estruturados importantes que atuam para compreender a dinâmica da utilização do espaço urbano por ciclistas e orientar a criação de políticas públicas de ciclomobilidade e segurança no trânsito. Neste estudo, propomos um sistema embarcado móvel para detecção e contagem de ciclistas que busca ser uma solução leve utilizando a visão computacional e métodos deep learning e tem por característica ser de baixo consumo de energia e fácil manuseio, baseado nas plataformas [Raspberry Pi 4](https://www.raspberrypi.com/) e o acelerador [Edge Tpu Coral](https://www.coral.ai/products/accelerator/). O sistema desenvolvido apresentou um desempenho `F1-score` de `0,9137` para o processamento de vídeo pré-gravado. Em experimentos de contagem em campo, onde a contagem realizada pelo sistema foi comparada com a contagem humana, resultou em uma performance de contagem entre `78,3%` e `82,2%` em relação à contagem visual.

> [!NOTE]
> A dissertação pode ser encontrada no repositório [RIUT UTFPR](http://repositorio.utfpr.edu.br/jspui/handle/1/34427)
> O artigo em [Journal of the Brazilian Computer Society](https://doi.org/10.5753/jbcs.2026.4937)

### Autor 
* Leandro Alves dos Santos

### Orientador
* Prof. Dr. Roberto Cesar Betini

### Coorientador
* Prof. Dr. Bogdan Tomoyuki Nassu

## Instalação e uso

Para o desenvolvimento e treinamento do modelo YOLOv8, foi utilizado o sistema operacional [Ubuntu 22.04](https://ubuntu.com/), e para testes em campo, foi utilizada a placa Raspberry Pi 4 com o sistema [Raspbian](https://www.raspberrypi.com/software/). As mesmas versões de bibliotecas de software livre foram utilizadas em ambos os sistemas.

O sistema desenvolvido é baseado nas seguintes linguagens de programação e bibliotecas:

| # |  Versão   |
|-|-|
| [Python](https://www.python.org/)                                        | 3.9       |
| [TensorFlow](https://www.tensorflow.org/install?hl=pt-br)                | 2.11.0    |
| [Ultralitcs](https://docs.ultralytics.com/pt)                            | 8.0149    |
| [PyTorch](https://pytorch.org/get-started/locally/)                      | 1.13.0    |
| [Cuda](https://docs.nvidia.com/cuda/cuda-quick-start-guide/index.html#x86-64-conda)                                                         | 11.7.1    |  
| [Coral](https://www.coral.ai/docs/accelerator/get-started/#requirements) | -         |
| [Gstream](https://gstreamer.freedesktop.org/)                            | 1.24.5    |

As configurações padrão do sistema podem ser editadas no arquivo `config.py`. O modelo pode ser selecionado conforme o hardware disponível, comentando ou descomentando a linha que contém a variável `MODEL_PATH`.

Se a máquina estiver equipada com GPU, o modelo `best.pt` é mais adequado; caso contrário, o modelo `best_full_integer_quant.tflite` é otimizado para execução em CPU. No Raspberry Pi, o modelo `best_full_integer_quant_edgetpu.tflite` apresenta melhor desempenho de processamento. Os modelos `.tflite` são quantizados para 8 bits.

Para executar o sistema de predição em imagens ou vídeo em um desktop ou notebook, pode-se utilizar o seguinte comando:

```
cd det-cicle
python ciclist-predict.py --mode=video
```

Outras variáveis também podem ser passadas como parâmetros via CLI.

As seguintes tags são aceitas:

```
  --iou: IOU (default: '0.5')
  
  --conf: Confidence (default: '0.5') 
  
  --imgsz: Image Size (default: '416')
  
  --mode: Modo de operação do sistema: image, video ou capture
  
  --path: Local para carregar os arquivos de imagens ou vídeo
  
  --result: Local para salvar o resultado
  
  --[no]save: Salvar inferências em vídeo pré-gravado (default: 'false')
  
  --time: Tempo de captura em segundos pelo sistema (default: '60.0')

  --[no]debug: Modo de depuração (default: 'false')
```

No Raspberry Pi 4, deve ser passado `--mode=capture` para predição a partir de uma captura pela câmera de vídeo. 
```
python ciclist-predict.py --mode=capture
```

O sistema foi desenvolvido apenas com a câmera [Rapberry Pi Camera](https://www.raspberrypi.com/products/camera-module-3/). Outros modelos de câmeras USB podem ser utilizados, com as adaptações necessárias no código.

Em campo, o sistema pode ser iniciado por meio de diversas possibilidades, em conjunto com o sistema operacional. Uma das formas mais práticas é incluir o comando no arquivo `.bashrc`. Outra possibilidade é conectar-se à Raspberry Pi via `SSH` utilizando um tablet ou mesmo um celular e, então, iniciar manualmente.

O módulo de carga utilizado foi a placa [`52PI`](https://wiki.52pi.com/index.php?title=EP-0118). Uma cópia da implementação para leitura do estado das baterias utilizando este módulo está disponível no pacote ups.

## Demonstração e testes
[![](https://img.youtube.com/vi/4Omx1HFKCNg/maxresdefault.jpg)](https://youtu.be/4Omx1HFKCNg)

[![](https://img.youtube.com/vi/N8ai5nzdK3I/maxresdefault.jpg)](https://youtu.be/N8ai5nzdK3I)

## Montagem
| | |
|-|-|
| ![](./assets/2433.jpg) | ![](./assets/2518.jpg)  |

| | |
|-|-|
| ![](./assets/4040.jpg) | ![](./assets/3538.jpg)  |


| | | |
|-|-|-|
| ![](./assets/3104.jpg) | ![](./assets/3134.jpg)  | ![](./assets/3215.jpg)  |
