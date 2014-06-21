# -*- coding: utf-8 -*-
#Python 2.7

import os, sys

from PySide import QtCore, QtGui

#############################################################################
class ColorSyntax(QtGui.QSyntaxHighlighter):

    #========================================================================
    def __init__(self, parent=None):
        super(ColorSyntax, self).__init__(parent)

        # liste des règles: [[regex, format], [regex, format], ...]
        self.regles = []

        #--------------------------------------------------------------------
        # coloration des mots clés Python
        motcles_format = QtGui.QTextCharFormat()
        motcles_format.setForeground(QtCore.Qt.blue) # mots clés en bleu
        #motcles_format.setFontWeight(QtGui.QFont.Bold) # pour mise en gras
        # liste des mots à considérer
        motcles_motifs = ['and', 'as', 'assert', 'break', 'class', 'continue',
                          'def', 'del', 'elif', 'else', 'except', 'exec',
                          'finally', 'for', 'from', 'global', 'if', 'import',
                          'in', 'is', 'lambda', 'not', 'or', 'pass', 'print',
                          'raise', 'return', 'try', 'while', 'with', 'yield']
        motcles_motifs += ["str", "int", "float", "None"]
        motcles_motifs += ["True", "False"]
        # enregistrement dans la liste des règles
        for motcles_motif in motcles_motifs:
            motcles_regex = QtCore.QRegExp("\\b" + motcles_motif + "\\b",
                                                    QtCore.Qt.CaseInsensitive)
            self.regles.append([motcles_regex, motcles_format])

        #--------------------------------------------------------------------
        # nombre entier ou flottant
        nombre_format = QtGui.QTextCharFormat()
        nombre_format.setForeground(QtCore.Qt.darkGreen)
        nombre_motif =  "\\b[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\\b"
        nombre_regex = QtCore.QRegExp(nombre_motif)
        nombre_regex.setMinimal(True)
        self.regles.append([nombre_regex, nombre_format])

        #--------------------------------------------------------------------
        # chaine de caractères simple quote: '...'
        chaine1_format = QtGui.QTextCharFormat()
        chaine1_format.setForeground(QtCore.Qt.green)#red)
        chaine1_motif = "\'.*\'"
        chaine1_regex = QtCore.QRegExp(chaine1_motif)
        chaine1_regex.setMinimal(True)
        self.regles.append([chaine1_regex, chaine1_format])

        #--------------------------------------------------------------------
        # chaine de caractères double quotes: "..."
        chaine2_format = QtGui.QTextCharFormat()
        chaine2_format.setForeground(QtCore.Qt.red)
        chaine2_motif = '\".*\"'
        chaine2_regex = QtCore.QRegExp(chaine2_motif)
        chaine2_regex.setMinimal(True)
        self.regles.append([chaine2_regex, chaine2_format])

        #--------------------------------------------------------------------
        # delimiteur: parenthèses, crochets, accolades
        delimiteur_format = QtGui.QTextCharFormat()
        delimiteur_format.setForeground(QtCore.Qt.red)
        delimiteur_motif = "[\)\(]+|[\{\}]+|[][]+"
        delimiteur_regex = QtCore.QRegExp(delimiteur_motif)
        self.regles.append([delimiteur_regex, delimiteur_format])

        #--------------------------------------------------------------------
        # commentaire sur une seule ligne et jusqu'à fin de ligne: ##...\n
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtCore.Qt.gray)
        comment_motif = "#[^\n]*"
        comment_regex = QtCore.QRegExp(comment_motif)
        self.regles.append([comment_regex, comment_format])

        #--------------------------------------------------------------------
        # commentaires multi-lignes: """..."""
        self.commentml_format = QtGui.QTextCharFormat()
        self.commentml_format.setForeground(QtCore.Qt.gray)

        self.commentml_deb_regex = QtCore.QRegExp('"""*')
        self.commentml_fin_regex = QtCore.QRegExp('\\*"""')

    #========================================================================
    def highlightBlock(self, text):
        """analyse chaque ligne et applique les règles"""

        # analyse des lignes avec les règles
        for expression, tformat in self.regles:
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, tformat)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        #pour les commentaires multilignes: """ ... """
        startIndex = 0
        if self.previousBlockState()!=1:
            startIndex = self.commentml_deb_regex.indexIn(text)

        while startIndex>=0:
            endIndex = self.commentml_fin_regex.indexIn(text, startIndex)
            if endIndex==-1:
                self.setCurrentBlockState(1)
                commentml_lg = len(text)-startIndex
            else:
                commentml_lg = endIndex-startIndex + \
                                       self.commentml_fin_regex.matchedLength()

            self.setFormat(startIndex, commentml_lg, self.commentml_format)

            startIndex = self.commentml_deb_regex.indexIn(text,
                                                       startIndex+commentml_lg)
