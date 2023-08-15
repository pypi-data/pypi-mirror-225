from typing import Iterable
from geneweaver.core.schema.gene import GeneValue


def gene_list_str(gene_ids: Iterable[GeneValue]) -> str:
    """Render a list of GeneValue objects to a string."""
    return "\n".join((f"{gene_value.symbol}\t{gene_value.value}"
                      for gene_value in gene_ids))

