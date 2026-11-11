from Bio import Entrez, SeqIO, AlignIO, Align
from Bio.Blast import NCBIWWW
from Bio.Seq import Seq
from Bio import motifs
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
import subprocess
import tempfile
import re

class IP3RAnalyzer:
    """Comprehensive IP3R sequence and domain analyzer"""

    def __init__(self, email: str):
        """Initialize with email for NCBI"""
        Entrez.email = email
        self.sequences = {}
        self.alignments = {}

        # Known IP3R domains and motifs
        self.domains = {
            'IP3_binding': (224, 604),  # IP3 binding core
            'calcium_binding': [(2230, 2749)],  # Ca2+ binding regions
            'channel_region': (2398, 2589),  # Ion channel domain
            'suppressor': (1574, 1654),  # Suppressor domain
            'regulatory': [(918, 1207), (1574, 1654)]  # Regulatory domains
        }

        # Calcium binding motifs (regular expressions; PROSITE style D-[DNS]-[DNS]-[DNS])
        self.ca_motifs = [
            'D[DNS][DNS][DNS]',  # EF-hand like
            '[DE][LIVMFYW][DNS][DNS]'  # Modified EF-hand
        ]

    def fetch_homologs(self, species: List[str]) -> Dict:
        """Fetch IP3R1 sequences from multiple species"""
        sequences = {}
        for sp in species:
            try:
                # Search for IP3R1 in species
                term = f"ITPR1[gene] AND {sp}[organism]"
                handle = Entrez.esearch(db="nucleotide", term=term)
                record = Entrez.read(handle)

                if record["Count"] != "0":
                    seq_handle = Entrez.efetch(db="nucleotide",
                                             id=record["IdList"][0],
                                             rettype="fasta",
                                             retmode="text")
                    sequences[sp] = SeqIO.read(seq_handle, "fasta")
                    seq_handle.close()

                handle.close()
            except Exception as e:
                print(f"Error fetching {sp}: {e}")

        self.sequences = sequences
        return sequences

    def analyze_domains(self, sequence: str) -> Dict:
        """Analyze domain conservation and properties"""
        results = {}

        for domain_name, domain_pos in self.domains.items():
            # Handle both single tuples and lists of tuples
            if isinstance(domain_pos, tuple):
                domain_positions = [domain_pos]
            else:
                domain_positions = domain_pos

            # Process each region of the domain
            domain_results = []
            for start, end in domain_positions:
                if end <= len(sequence):
                    domain_seq = sequence[start:end]

                    domain_results.append({
                        'length': len(domain_seq),
                        'gc_content': (domain_seq.count('G') +
                                     domain_seq.count('C')) / len(domain_seq),
                        'hydrophobicity': self._calculate_hydrophobicity(domain_seq),
                        'conservation': self._calculate_conservation(domain_seq)
                    })

            # Combine results if multiple regions
            if domain_results:
                results[domain_name] = domain_results[0] if len(domain_results) == 1 \
                                     else {
                    'regions': domain_results,
                    'total_length': sum(r['length'] for r in domain_results),
                    'average_conservation': sum(r['conservation'] for r in domain_results) / len(domain_results) \
                                         if any(r['conservation'] is not None for r in domain_results) else None
                }
                if len(domain_results) > 1:
                    # same keys as single-region domains, for callers that read 'length'/'conservation'
                    results[domain_name]['length'] = results[domain_name]['total_length']
                    results[domain_name]['conservation'] = results[domain_name]['average_conservation']

        return results

    def _calculate_hydrophobicity(self, sequence: str) -> float:
        """Calculate average hydrophobicity using Kyte-Doolittle scale"""
        kd_scale = {
            'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
            'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
            'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
            'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
        }

        aa_seq = str(Seq(sequence).translate())
        total = sum(kd_scale.get(aa, 0) for aa in aa_seq)
        return total / len(aa_seq)

    def _calculate_conservation(self, sequence: str) -> float:
        """Calculate sequence conservation across species"""
        if not self.sequences:
            return None

        # Simple conservation score based on identical positions
        conserved = 0
        total = 0

        # Convert SeqRecord objects to strings for comparison
        seq_strings = {species: str(seq.seq) for species, seq in self.sequences.items()}

        for pos in range(0, len(sequence), 3):
            if pos + 3 > len(sequence):
                break

            codon = sequence[pos:pos+3]
            # Compare with sequence strings instead of SeqRecord objects
            if all(len(seq_str) > pos+2 and seq_str[pos:pos+3] == codon
                  for seq_str in seq_strings.values()):
                conserved += 1
            total += 1

        return conserved / total if total > 0 else 0

    def find_calcium_binding_sites(self, sequence: str) -> List[Dict]:
        """Identify potential calcium binding sites"""
        sites = []

        # Convert DNA to protein sequence
        protein_seq = str(Seq(sequence).translate())

        for motif_pattern in self.ca_motifs:
            matches = re.finditer(motif_pattern, protein_seq)
            for match in matches:
                sites.append({
                    'motif': motif_pattern,
                    'position': match.start(),
                    'sequence': match.group(),
                    'in_known_domain': any(start <= match.start()*3 <= end
                                         for start, end in self.domains['calcium_binding'])
                })

        return sites

    def analyze_splice_variants(self, species: str = "Homo sapiens") -> Dict:
        """Analyze known splice variants"""
        try:
            # Search for splice variants
            term = f"ITPR1[gene] AND {species}[organism] AND variant"
            handle = Entrez.esearch(db="nucleotide", term=term)
            record = Entrez.read(handle)
            handle.close()

            variants = {}
            for id in record["IdList"]:
                seq_handle = Entrez.efetch(db="nucleotide", id=id,
                                         rettype="gb", retmode="text")
                variant_record = SeqIO.read(seq_handle, "genbank")
                seq_handle.close()

                variants[variant_record.id] = {
                    'length': len(variant_record.seq),
                    'description': variant_record.description,
                    'features': [feat for feat in variant_record.features
                               if feat.type in ['CDS', 'exon', 'variation']]
                }

            return {
                'count': len(variants),
                'variants': variants,
                'length_variation': {
                    'min': min(v['length'] for v in variants.values()),
                    'max': max(v['length'] for v in variants.values()),
                    'average': sum(v['length'] for v in variants.values()) / len(variants)
                }
            }

        except Exception as e:
            print(f"Error analyzing splice variants: {e}")
            return None

    def visualize_domains(self) -> None:
        """Create visualization of domain structure and conservation"""
        if not self.sequences:
            print("No sequences loaded for visualization")
            return

        plt.figure(figsize=(15, 10))

        # Domain structure plot
        plt.subplot(3, 1, 1)
        domain_colors = {
            'IP3_binding': 'red',
            'calcium_binding': 'blue',
            'channel_region': 'green',
            'suppressor': 'yellow',
            'regulatory': 'purple'
        }

        y_pos = 0
        for domain, positions in self.domains.items():
            # Convert single tuple to list of tuples for consistent handling
            if isinstance(positions, tuple):
                positions = [positions]

            # Plot each region of the domain
            for start, end in positions:
                plt.barh(y_pos, end - start, left=start,
                        color=domain_colors[domain], alpha=0.6,
                        label=domain if y_pos == list(self.domains.keys()).index(domain) else "")
            y_pos += 1

        plt.yticks(range(len(self.domains)), list(self.domains.keys()))
        plt.xlabel('Sequence Position')
        plt.title('IP3R Domain Structure')
        plt.legend()

        # Conservation plot
        plt.subplot(3, 1, 2)
        conservation_scores = [self._calculate_conservation(str(seq.seq))
                             for seq in self.sequences.values()]
        plt.plot(range(len(conservation_scores)), conservation_scores)
        plt.xlabel('Position')
        plt.ylabel('Conservation Score')
        plt.title('Sequence Conservation')

        # Calcium binding sites
        plt.subplot(3, 1, 3)
        ca_sites = self.find_calcium_binding_sites(str(list(self.sequences.values())[0].seq))
        positions = [site['position'] for site in ca_sites]
        plt.hist(positions, bins=50)
        plt.xlabel('Position')
        plt.ylabel('Number of Ca2+ Binding Motifs')
        plt.title('Distribution of Calcium Binding Motifs')

        plt.tight_layout()
        plt.show()

    def compare_species(self, species_list: List[str]) -> Dict:
        """Compare IP3R1 across species"""
        # Fetch sequences if not already present
        if not self.sequences:
            self.fetch_homologs(species_list)

        comparisons = {}
        reference_seq = str(list(self.sequences.values())[0].seq)

        for sp1 in species_list:
            if sp1 not in self.sequences:
                continue

            seq1 = str(self.sequences[sp1].seq)
            comparisons[sp1] = {
                'length': len(seq1),
                'identity_to_reference': self._calculate_identity(reference_seq, seq1),
                'domain_conservation': self.analyze_domains(seq1),
                'calcium_sites': len(self.find_calcium_binding_sites(seq1))
            }

        return comparisons

    def _calculate_identity(self, seq1: str, seq2: str) -> float:
        """Calculate sequence identity between two sequences"""
        if len(seq1) != len(seq2):
            return 0

        matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
        return matches / len(seq1)

    def visualize_species_comparison(self, comparisons: Dict) -> None:
        """Visualize species comparison results"""
        plt.figure(figsize=(15, 10))

        # Sequence identity plot
        plt.subplot(2, 2, 1)
        species = list(comparisons.keys())
        identities = [comp['identity_to_reference'] for comp in comparisons.values()]
        plt.bar(species, identities)
        plt.xticks(rotation=45)
        plt.ylabel('Identity to Reference')
        plt.title('Sequence Conservation Across Species')

        # Domain conservation plot
        plt.subplot(2, 2, 2)
        domain_cons = {domain: [comp['domain_conservation'][domain]['conservation']
                              for comp in comparisons.values()]
                      for domain in self.domains}

        x = np.arange(len(species))
        width = 0.15
        for i, (domain, scores) in enumerate(domain_cons.items()):
            plt.bar(x + i*width, scores, width, label=domain)

        plt.xticks(x + width*2, species, rotation=45)
        plt.ylabel('Domain Conservation')
        plt.title('Domain Conservation by Species')
        plt.legend()

        # Calcium binding sites
        plt.subplot(2, 2, 3)
        ca_sites = [comp['calcium_sites'] for comp in comparisons.values()]
        plt.bar(species, ca_sites)
        plt.xticks(rotation=45)
        plt.ylabel('Number of Ca2+ Binding Sites')
        plt.title('Calcium Binding Sites by Species')

        plt.tight_layout()
        plt.show()

def analyze_ip3r_comprehensive(email: str):
    """Run comprehensive analysis of IP3R"""
    analyzer = IP3RAnalyzer(email)

    # Species to compare
    species_list = [
        "Homo sapiens",
        "Mus musculus",
        "Rattus norvegicus",
        "Danio rerio",
        "Drosophila melanogaster"
    ]

    # Fetch sequences
    print("Fetching sequences...")
    sequences = analyzer.fetch_homologs(species_list)

    # Analyze domains
    print("\nAnalyzing domains...")
    human_seq = str(sequences["Homo sapiens"].seq)
    domain_analysis = analyzer.analyze_domains(human_seq)

    # Find calcium binding sites
    print("\nIdentifying calcium binding sites...")
    ca_sites = analyzer.find_calcium_binding_sites(human_seq)

    # Analyze splice variants
    print("\nAnalyzing splice variants...")
    variants = analyzer.analyze_splice_variants()

    # Compare species
    print("\nComparing across species...")
    comparisons = analyzer.compare_species(species_list)

    # Generate visualizations
    print("\nGenerating visualizations...")
    analyzer.visualize_domains()
    analyzer.visualize_species_comparison(comparisons)

    return {
        'domain_analysis': domain_analysis,
        'calcium_sites': ca_sites,
        'splice_variants': variants,
        'species_comparison': comparisons
    }

if __name__ == "__main__":
    # Replace with your email
    results = analyze_ip3r_comprehensive("george.dickinson@gmail.com")
