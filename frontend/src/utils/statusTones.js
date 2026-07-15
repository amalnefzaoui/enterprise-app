// Mappe chaque statut métier (RH, Achat/Vente, Formation) à un "tone" de badge cohérent
const TONE_MAP = {
  // Congés
  'en_attente': 'warning',
  'approuvé': 'success',
  'refusé': 'danger',
  // Pointage
  'présent': 'success',
  'retard': 'warning',
  'absent': 'danger',
  'congé': 'neutral',
  // Commandes achat
  'brouillon': 'neutral',
  'envoyée': 'warning',
  'reçue': 'success',
  'annulée': 'danger',
  // Commandes vente
  'confirmée': 'warning',
  'livrée': 'success',
  // Factures
  'payée': 'success',
  'impayée': 'warning',
  'en_retard': 'danger',
  // Formations
  'non_commencé': 'neutral',
  'en_cours': 'warning',
  'terminé': 'success',
  // Employés / fournisseurs / clients
  'actif': 'success',
  'inactif': 'neutral'
}

export function statusTone(status) {
  return TONE_MAP[status] || 'neutral'
}
