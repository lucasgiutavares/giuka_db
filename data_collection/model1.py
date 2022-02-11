from PyPDF2 import PdfFileReader
import re, os, json

def get_block(txt, begin=False, end=False):
    if begin:
        txt = txt[txt.find(begin) + len(begin):]

    if end:
        txt = txt[:txt.find(end)]

    return txt

def game_data(pdf_path):
    f = open(pdf_path, "rb")
    pdf = PdfFileReader(f)
    pdf_text = pdf.getPage(0).extractText()

    # Data Dictionary
    game_data_dict = {
        'game_data': {},
        'referee_data': {}
    }

    # First Game Data Block
    block1 = get_block(pdf_text, 'Categoria:', 'ARBITRAGEM')

    game_data_dict['game_data']['category'] = get_block(block1, '', 'Rodada:')
    game_data_dict['game_data']['game'] = get_block(block1, 'Rodada:', 'Campeonato:').strip()
    game_data_dict['game_data']['champ'] = get_block(block1, 'Campeonato:', 'Data:')
    game_data_dict['game_data']['date'] = get_block(block1, 'Data:', 'Horário:')
    game_data_dict['game_data']['time'] = get_block(block1, 'Horário:', 'Local:').strip()
    game_data_dict['game_data']['place'] = get_block(block1, 'Local:')

    # Referee Block
    block2 = get_block(pdf_text, 'ARBITRAGEM', 'DADOS DO JOGO')

    game_data_dict['referee_data']['ref'] = get_block(block2, 'Arbitro:', 'Arbitro Assistente 1:')
    game_data_dict['referee_data']['assRef1'] = get_block(block2, 'Arbitro Assistente 1:', 'Arbitro Assistente 2:')
    game_data_dict['referee_data']['assRef2'] = get_block(block2, 'Arbitro Assistente 2:', 'Quarto Arbitro:')
    game_data_dict['referee_data']['fourthRef'] = get_block(block2, 'Quarto Arbitro:')

    # Second Game Data Block
    block3 = get_block(pdf_text, 'DADOS DO JOGO', 'ESCALAÇÃO')
    game_data_dict['game_data']['home1H'] = get_block(block3, 'MANDANTEEntrada no 1º tempo:', 'Entrada no 2º tempo:').strip()
    game_data_dict['game_data']['home2H'] = get_block(block3, 'Entrada no 2º tempo:', 'VISITANTE').strip()
    game_data_dict['game_data']['away1H'] = get_block(block3, 'VISITANTEEntrada no 1º tempo:', 'Entrada no 2º tempo:').strip()
    game_data_dict['game_data']['away2H'] = get_block(get_block(block3, 'VISITANTE'), 'Entrada no 2º tempo:', 'Início do 1º Tempo:').strip()
    game_data_dict['game_data']['begin1H'] = get_block(block3, 'Início do 1º Tempo:', 'Término do 1º Tempo:').strip()
    game_data_dict['game_data']['end1H'] = get_block(block3, 'Término do 1º Tempo:', 'Resultado do 1º Tempo:').strip()
    game_data_dict['game_data']['result1H'] = get_block(block3, 'Resultado do 1º Tempo:', 'Início do 2º Tempo:').strip()
    game_data_dict['game_data']['begin2H'] = get_block(block3, 'Início do 2º Tempo:', 'Término do 2º Tempo:').strip()
    game_data_dict['game_data']['end2H'] = get_block(block3, 'Término do 2º Tempo:', 'Resultado Final:').strip()
    game_data_dict['game_data']['result2H'] = get_block(block3, 'Resultado Final:', 'Acréscimo 1º Tempo:').strip()
    game_data_dict['game_data']['extra1H'] = get_block(block3, 'Acréscimo 1º Tempo:', 'Acréscimo 2º Tempo:').strip()
    game_data_dict['game_data']['extra2H'] = get_block(block3, 'Acréscimo 2º Tempo:', 'Obs:').strip()

    return json.dumps(game_data_dict)

# json_list = []
# dir_path = 'data/original/dockets/'
# final_dir = 'data/preprocessed/json/'
# for f in os.listdir(dir_path):
#     json.dump(game_data(dir_path + f), open(final_dir + f.replace('.pdf', '.json'), 'w'))