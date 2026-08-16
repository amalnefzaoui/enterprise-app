# Synco — RH & Achat/Vente (stage 2ème année Licence)

Architecture microservices : **Python (FastAPI)** pour l'API métier RH + Achat/Vente, **Node.js** pour le service de formation (remplace Moodle), **Vue.js** pour le frontend.

## Pourquoi pas Moodle ?

Moodle est un LMS (PHP) axé formation — il ne couvre ni la gestion RH (congés, pointage) ni l'achat/vente. Ici, le "training-service" en Node.js remplace la brique formation par un module simple et sur-mesure (cours, inscriptions, suivi de progression), tout en gardant l'esprit "suivi de formation" du sujet de stage.

## Architecture

```
┌──────────────┐      ┌────────────────────┐      ┌──────────────┐
│  Frontend     │ ───► │  Python API          │ ───► │  MySQL        │
│  Vue.js       │ ◄─── │  (FastAPI)           │ ◄─── │  (hr_gestion) │
│  (port 5173)  │      │  (port 8000)         │      └──────────────┘
└──────────────┘      └────────────────────┘
       │                        
       │              ┌──────────────┐      ┌──────────────┐
       └────────────► │  Training     │ ───► │  MySQL        │
                       │  Service       │ ◄─── │  (training_db)│
                       │  (Node.js)     │      └──────────────┘
                       │  (port 5000)   │
                       └──────────────┘
```

## Contenu du projet

```
enterprise-app/
├── docker-compose.yml
├── python-api/                  # API RH + Achat/Vente (FastAPI)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── app/
│       ├── main.py              # Point d'entrée
│       ├── config.py            # Configuration (variables d'env)
│       ├── database.py          # Connexion SQLAlchemy
│       ├── models/              # Modèles SQLAlchemy (11 tables)
│       ├── schemas/              # Schémas Pydantic (validation)
│       ├── auth/                 # Sécurité JWT + dépendances
│       └── routers/              # Endpoints FastAPI
│           ├── auth.py, employees.py, leaves.py, attendance.py     (RH)
│           └── products.py, suppliers.py, customers.py,
│               purchase_orders.py, sales_orders.py, invoices.py     (Achat/Vente)
├── training-service/             # Service formation (Node.js — remplace Moodle)
│   ├── Dockerfile
│   ├── package.json
│   ├── .env.example
│   └── src/
│       ├── server.js
│       ├── config/database.js
│       ├── models/Course.js, Enrollment.js
│       └── routes/courses.js, enrollments.js
└── frontend/                     # Dashboard Vue.js
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    ├── .env.example
    └── src/
        ├── main.js, App.vue
        ├── router/index.js        # Routes protégées par auth
        ├── stores/auth.js         # État global (Pinia)
        ├── services/               # Clients axios (Python API + Training)
        ├── components/
        │   ├── AppLayout.vue      # Sidebar + navigation
        │   └── StatusPill.vue     # Badge de statut réutilisable
        ├── utils/statusTones.js   # Mapping statut → couleur
        └── views/                 # 12 vues (Dashboard, Employees, Leaves...)
```

## Démarrage

```bash
cd enterprise-app
docker compose up -d --build
```

⏳ Premier démarrage : ~1-2 minutes (téléchargement images MySQL + build Python/Node).

Ça démarre :
- **Frontend Vue.js** → http://localhost:5173 (l'application à ouvrir dans le navigateur)
- **API Python** → http://localhost:8000 (docs interactives auto-générées → http://localhost:8000/docs)
- **Training Service** → http://localhost:5000
- 2 bases MySQL (`db-api` sur port 3307, `db-training` sur port 3308)

### Premier démarrage — créer un compte admin
L'interface Vue ne propose pas d'inscription (par sécurité). Crée le premier compte admin via curl ou `/docs` :
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@entreprise.com","password":"AdminPass123!","role":"admin"}'
```
Puis connecte-toi sur http://localhost:5173 avec ces identifiants.

### Documentation API interactive (Swagger)
FastAPI génère automatiquement une doc interactive : **http://localhost:8000/docs** — tu peux tester chaque endpoint directement depuis le navigateur, sans Postman/curl.

## Tester rapidement

```bash
# Santé des 2 services
curl http://localhost:8000/api/health
curl http://localhost:5000/api/health

# Créer un compte admin
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@entreprise.com","password":"AdminPass123!","role":"admin"}'

# Se connecter → récupère un token JWT
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@entreprise.com","password":"AdminPass123!"}'

# Créer un employé (avec le token)
curl -X POST http://localhost:8000/api/employees/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -d '{"first_name":"Amal","last_name":"Nefzaoui","email":"amal@entreprise.com"}'

# Créer un compte RH
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"rh@synco.tn","password":"RhPass123!","role":"rh"}'

# Créer un compte Manager (Achat/Vente)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"achatvente@synco.tn","password":"AvPass123!","role":"manager"}'

# Créer une formation (training-service)
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"title":"Sécurité informatique","category":"IT","durationHours":8}'
```

## Rôles & permissions (API Python)

4 rôles : `admin` (tout), `rh` (RH uniquement), `manager` (Achat/Vente uniquement), `employee` (accès basique).

| Route | Rôle requis |
|---|---|
| POST /api/employees | admin, rh |
| PUT /api/employees/:id | admin, rh |
| DELETE /api/employees/:id | admin, rh |
| PATCH /api/leaves/:id/status | admin, rh |
| GET /api/leaves | filtré automatiquement pour `employee` (ses propres congés uniquement) |
| GET /api/attendance/report | filtré automatiquement pour `employee` (son propre pointage uniquement) |
| POST/PUT/DELETE /api/products | admin, manager |
| PATCH /api/products/:id/stock | admin, manager |
| POST/PUT/DELETE /api/suppliers, /customers | admin, manager |
| PATCH /api/purchase-orders/:id/status | admin, manager |
| PATCH /api/sales-orders/:id/status | admin, manager |
| POST/PATCH /api/invoices | admin, manager |

Le frontend masque aussi les menus/pages selon le rôle (RH et Achat/Vente sont mutuellement invisibles), et le routeur Vue bloque l'accès direct par URL.

**Limite connue** : les routes GET (lecture) de produits/fournisseurs/clients/commandes/factures ne sont pas protégées côté API (accessibles via `/docs` même sans le bon rôle) — seule l'interface les masque.

## Logique métier clé

- **Congés** : calcul automatique des jours ouvrés, vérification du solde, déduction à l'approbation.
- **Commande d'achat** : passage à `reçue` → incrémentation automatique du stock.
- **Commande de vente** : vérification du stock à la création, décrémentation à la confirmation (`confirmée`).
- **Facture** : générée depuis une commande existante, numéro auto (`FA-2026-xxxxxx` / `FV-2026-xxxxxx`).
- **Formation** : suivi de progression (%) et complétion par employé, résumé global via `/api/enrollments/employee/:id/summary`.

## Endpoints disponibles

### API Python (port 8000)
| Méthode | Route | Description |
|---|---|---|
| POST | /api/auth/register, /login | Authentification |
| GET | /api/auth/me | Utilisateur connecté |
| GET/POST/PUT/DELETE | /api/employees | CRUD employés |
| GET/POST | /api/leaves | Congés |
| PATCH | /api/leaves/{id}/status | Approuver/refuser |
| POST | /api/attendance/checkin, /checkout | Pointage |
| GET | /api/attendance/report | Rapport présence |
| GET/POST/PUT/DELETE | /api/products | Produits/stock |
| PATCH | /api/products/{id}/stock | Ajustement stock |
| GET/POST/PUT/DELETE | /api/suppliers, /customers | Fournisseurs/clients |
| GET/POST | /api/purchase-orders, /sales-orders | Commandes |
| PATCH | .../{id}/status | Changement statut (impacte le stock) |
| GET/POST/PATCH | /api/invoices | Facturation |

### Training Service (port 5000)
| Méthode | Route | Description |
|---|---|---|
| GET/POST/PUT/DELETE | /api/courses | CRUD formations |
| GET/POST | /api/enrollments | Inscriptions |
| PATCH | /api/enrollments/{id}/progress | Mise à jour progression |
| GET | /api/enrollments/employee/{id}/summary | Résumé formations d'un employé |

## Prochaines étapes

1. ~~Frontend Vue.js~~ ✅ fait (12 vues : Dashboard, RH, Achat/Vente, Formations)
2. ~~Restriction fine par rôle~~ ✅ fait (backend filtre par `employee_id`, frontend masque les menus, routeur bloque les URLs directes)
3. **Sécuriser les routes GET** Achat/Vente et RH (actuellement lisibles via `/docs` sans restriction de rôle, seule l'UI les masque)
4. **Migrations Alembic** (Python) au lieu de `create_all` pour la gestion de schéma en production
5. **Rapports** : export PDF/Excel
6. **Page d'inscription** (actuellement via curl/`/docs` uniquement, par sécurité)
7. **Authentification sur le training-service** (Node.js) — actuellement 100% ouvert, sans vérification de token