"""Pacote de apoio das atividades avaliativas do Raio-X do Seu Negócio.

Cada atividade tem o **seu** kit, com o seu tema e o seu gerador de dados. O
notebook do aluno importa só o kit da atividade que está resolvendo::

    from scripts.kit_a01 import iniciar, prever, registrar, conferir, diario, assinatura

A mecânica compartilhada por todos os kits — semente pessoal, diário de bordo,
conferência, assinatura — mora em ``scripts/core.py``.
"""
