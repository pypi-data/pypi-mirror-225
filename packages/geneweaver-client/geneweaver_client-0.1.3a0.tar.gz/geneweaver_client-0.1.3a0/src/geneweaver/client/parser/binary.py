"""Parsing for Binary Genesets."""
from typing import List
from geneweaver.core.schema.gene import GeneValue


def gene_id_list(gene_ids: list) -> List[GeneValue]:
    """Parse a list of Gene IDs to GeneValue objects.

    :param gene_ids: List of Gene IDs.
    :return: List of GeneValue objects.
    """
    return [GeneValue(gene_id=gene_id, value=1) for gene_id in gene_ids]
