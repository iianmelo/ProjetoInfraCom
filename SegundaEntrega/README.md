# ProjetoInfraCom

INSTRUÇÕES PARA EXECUTAR:

1 - Abra dois terminais.

2 - Vá para o diretório `<Servidor>` em um terminal e `<Cliente>` no outro.

3 - Rode primeiro `python server.py` no `<Servidor>` e `python client.py` no `<Cliente>` em seguida.

4 - É necessário escolher o arquivo que será enviado pelo cliente. (p.ex. o aquivo `hello.txt` ou a imagem `Imagem.png`).

Após isso, o cliente enviará a mensagem para o servidor. Para cada segmento recebido, o servidor responderá com um ACK e o cliente somente envia o próximo segmento ao receber o ACK do segmento atual. Foi implementada uma perda randômica de pacotes com probabilidade de 10%, escolhida arbitrariamente para testes. Ao haver uma perda, ocorrerá um timeout pelo lado do cliente, e ele reenviará o segmento. A cada segmento enviado, aparece uma mensagem terminal do cliente indicando o envio e o número de sequência. A cada segmento recebido, aparece uma mensagem no terminal do servidor indicando o recebimento do segmento e o envio do ACK com o número de sequência. Ao haver uma perda proposital, é indicado no terminal do servidor que uma perda está sendo simulada, junto com o número de sequência do segmento "perdido". Ao haver um timeout, é indicado com uma mensagem no terminal do cliente, junto com o número de sequência do segmento que causou o timeout. 


INTEGRANTES:

- João Victor Fellows Rabêlo (@JoaoFellows)
- Rafael Alves de Azevedo Silva (@Azvedo)
- Guilherme Montenegro de Albuquerque (@GuilhermeMontt)
- Ian Medeiros Melo (@iianmelo)
- Henrique Lins Pereira Affonso de Amorim (@hlpaa)
