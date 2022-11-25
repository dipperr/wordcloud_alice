class Livro:
    def __init__(self, autor, titulo, subtitulo, preco, comentarios):
        self._autor = autor
        self._titulo = titulo
        self._subtitulo = subtitulo
        self._preco = self.remove_nbs(preco)
        self._comentarios = list(comentarios)
        self._hashe = hash(titulo)

    @property
    def autor(self):
        return self._autor

    @property
    def titulo(self):
        return self._titulo

    @property
    def subtitulo(self):
        return self._subtitulo

    @property
    def preco(self):
        return self._preco

    @property
    def comentarios(self):
        return self._comentarios

    @property
    def hashe(self):
        return self._hashe

    def remove_nbs(self, preco):
        """
        Remove o caractere No-break Space.
        Número 160 da tabela unicode
        """
        return ''.join([i for i in preco if ord(i) != 160])

    def json(self):
        return dict(
            autor=self.autor,
            titulo=self.titulo,
            subtitulo=self.subtitulo,
            preco=self.preco,
            comentarios=self.comentarios
        )

    def __str__(self):
        return "Autor: {0}\nTitulo: {1}\nSubtitulo: {2}\nPreco: {3}" \
            .format(self.autor, self.titulo, self.subtitulo, self.preco)

    def __eq__(self, outro):
        return self.hashe == outro.hashe
