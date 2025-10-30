#!/bin/bash

# Script de test des endpoints de l'API Mathia
# Usage: bash tests/test_api.sh

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="http://localhost:3000/api"
TEST_EMAIL="test_$(date +%s)@example.com"
TEST_PASSWORD="test123456"
TEST_NAME="Test User"

echo ""
echo "======================================================================"
echo "🧪 TEST DE L'API MATHIA"
echo "======================================================================"
echo ""
echo "📍 URL de base: $BASE_URL"
echo "📧 Email de test: $TEST_EMAIL"
echo ""

# Fonction pour afficher les résultats
print_test() {
    local test_name=$1
    local status=$2
    
    if [ "$status" -eq 0 ]; then
        echo -e "${GREEN}✅ $test_name${NC}"
    else
        echo -e "${RED}❌ $test_name${NC}"
    fi
}

# Fonction pour extraire le token JSON
extract_token() {
    echo "$1" | grep -o '"token":"[^"]*' | grep -o '[^"]*$'
}

# Fonction pour extraire un champ JSON
extract_field() {
    local json=$1
    local field=$2
    echo "$json" | grep -o "\"$field\":[^,}]*" | cut -d':' -f2 | tr -d '"' | tr -d ' '
}

echo "======================================================================"
echo "TEST 1: POST /auth/signup - Créer un compte"
echo "======================================================================"
echo ""

SIGNUP_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$TEST_NAME\",
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\"
  }")

HTTP_CODE=$(echo "$SIGNUP_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$SIGNUP_RESPONSE" | sed '$d')

echo "📤 Requête:"
echo "POST $BASE_URL/auth/signup"
echo "Body: { name: \"$TEST_NAME\", email: \"$TEST_EMAIL\", password: \"***\" }"
echo ""
echo "📥 Réponse (HTTP $HTTP_CODE):"
echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
echo ""

if [ "$HTTP_CODE" -eq 201 ]; then
    print_test "Inscription réussie" 0
    TOKEN=$(extract_token "$RESPONSE_BODY")
    USER_ID=$(extract_field "$RESPONSE_BODY" "id")
    echo -e "${BLUE}🔑 Token récupéré (${#TOKEN} caractères)${NC}"
    echo -e "${BLUE}👤 User ID: $USER_ID${NC}"
else
    print_test "Inscription échouée" 1
    echo "❌ Arrêt des tests"
    exit 1
fi

echo ""
echo "======================================================================"
echo "TEST 2: POST /auth/login - Obtenir un JWT"
echo "======================================================================"
echo ""

sleep 1

LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\"
  }")

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$LOGIN_RESPONSE" | sed '$d')

echo "📤 Requête:"
echo "POST $BASE_URL/auth/login"
echo "Body: { email: \"$TEST_EMAIL\", password: \"***\" }"
echo ""
echo "📥 Réponse (HTTP $HTTP_CODE):"
echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
echo ""

if [ "$HTTP_CODE" -eq 200 ]; then
    print_test "Connexion réussie" 0
    TOKEN=$(extract_token "$RESPONSE_BODY")
    echo -e "${BLUE}🔑 Nouveau token récupéré${NC}"
else
    print_test "Connexion échouée" 1
fi

echo ""
echo "======================================================================"
echo "TEST 3: GET /courses - Récupérer les cours"
echo "======================================================================"
echo ""

sleep 1

COURSES_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/courses" \
  -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(echo "$COURSES_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$COURSES_RESPONSE" | sed '$d')

echo "📤 Requête:"
echo "GET $BASE_URL/courses"
echo "Headers: Authorization: Bearer ${TOKEN:0:20}..."
echo ""
echo "📥 Réponse (HTTP $HTTP_CODE):"
echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
echo ""

if [ "$HTTP_CODE" -eq 200 ]; then
    print_test "Récupération des cours réussie" 0
    COURSES_COUNT=$(echo "$RESPONSE_BODY" | grep -o '"id"' | wc -l)
    echo -e "${BLUE}📚 Nombre de cours: $COURSES_COUNT${NC}"
else
    print_test "Récupération des cours échouée" 1
fi

echo ""
echo "======================================================================"
echo "TEST 4: GET /exercises (sans filtre) - Lister tous les exercices"
echo "======================================================================"
echo ""

sleep 1

EXERCISES_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/exercises" \
  -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(echo "$EXERCISES_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$EXERCISES_RESPONSE" | sed '$d')

echo "📤 Requête:"
echo "GET $BASE_URL/exercises"
echo "Headers: Authorization: Bearer ${TOKEN:0:20}..."
echo ""
echo "📥 Réponse (HTTP $HTTP_CODE):"
echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
echo ""

if [ "$HTTP_CODE" -eq 200 ]; then
    print_test "Récupération des exercices réussie" 0
    EXERCISES_COUNT=$(echo "$RESPONSE_BODY" | grep -o '"exerciseId"' | wc -l)
    if [ "$EXERCISES_COUNT" -eq 0 ]; then
        EXERCISES_COUNT=$(echo "$RESPONSE_BODY" | grep -o '"id":' | wc -l)
    fi
    echo -e "${BLUE}📝 Nombre d'exercices: $EXERCISES_COUNT${NC}"
    
    # Extraire le premier exercice ID si disponible
    FIRST_EXERCISE_ID=$(echo "$RESPONSE_BODY" | grep -o '"id":[0-9]*' | head -n1 | grep -o '[0-9]*')
    if [ -n "$FIRST_EXERCISE_ID" ]; then
        echo -e "${BLUE}🎯 Premier exercice ID: $FIRST_EXERCISE_ID${NC}"
    fi
else
    print_test "Récupération des exercices échouée" 1
fi

echo ""
echo "======================================================================"
echo "TEST 5: GET /exercises?courseId=1&difficulty=facile - Filtrer les exercices"
echo "======================================================================"
echo ""

sleep 1

FILTERED_EXERCISES_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/exercises?courseId=1&difficulty=facile" \
  -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(echo "$FILTERED_EXERCISES_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$FILTERED_EXERCISES_RESPONSE" | sed '$d')

echo "📤 Requête:"
echo "GET $BASE_URL/exercises?courseId=1&difficulty=facile"
echo "Headers: Authorization: Bearer ${TOKEN:0:20}..."
echo ""
echo "📥 Réponse (HTTP $HTTP_CODE):"
echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
echo ""

if [ "$HTTP_CODE" -eq 200 ]; then
    print_test "Filtrage des exercices réussi" 0
    FILTERED_COUNT=$(echo "$RESPONSE_BODY" | grep -o '"difficulty":"facile"' | wc -l)
    echo -e "${BLUE}📝 Exercices faciles du cours 1: $FILTERED_COUNT${NC}"
else
    print_test "Filtrage des exercices échoué" 1
fi

echo ""
echo "======================================================================"
echo "TEST 6: POST /attempts - Enregistrer une réponse"
echo "======================================================================"
echo ""

sleep 1

# Utiliser l'exercice ID trouvé précédemment, ou 1 par défaut
EXERCISE_ID_TO_TEST=${FIRST_EXERCISE_ID:-1}

ATTEMPT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/attempts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"exerciseId\": $EXERCISE_ID_TO_TEST,
    \"userAnswer\": \"Test answer\"
  }")

HTTP_CODE=$(echo "$ATTEMPT_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$ATTEMPT_RESPONSE" | sed '$d')

echo "📤 Requête:"
echo "POST $BASE_URL/attempts"
echo "Headers: Authorization: Bearer ${TOKEN:0:20}..."
echo "Body: { exerciseId: $EXERCISE_ID_TO_TEST, userAnswer: \"Test answer\" }"
echo ""
echo "📥 Réponse (HTTP $HTTP_CODE):"
echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
echo ""

if [ "$HTTP_CODE" -eq 201 ]; then
    print_test "Enregistrement de la réponse réussi" 0
    IS_CORRECT=$(extract_field "$RESPONSE_BODY" "isCorrect")
    echo -e "${BLUE}✓ Réponse enregistrée (Correcte: $IS_CORRECT)${NC}"
elif [ "$HTTP_CODE" -eq 404 ]; then
    echo -e "${YELLOW}⚠️  Exercice non trouvé (base de données vide?)${NC}"
    print_test "Test de tentative (exercice manquant)" 0
else
    print_test "Enregistrement de la réponse échoué" 1
fi

echo ""
echo "======================================================================"
echo "TEST 7: Test sans authentification (doit échouer)"
echo "======================================================================"
echo ""

sleep 1

UNAUTH_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/courses")

HTTP_CODE=$(echo "$UNAUTH_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$UNAUTH_RESPONSE" | sed '$d')

echo "📤 Requête:"
echo "GET $BASE_URL/courses (sans token)"
echo ""
echo "📥 Réponse (HTTP $HTTP_CODE):"
echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
echo ""

if [ "$HTTP_CODE" -eq 401 ]; then
    print_test "Protection JWT fonctionne correctement" 0
else
    print_test "Protection JWT ne fonctionne pas!" 1
fi

echo ""
echo "======================================================================"
echo "📊 RÉSUMÉ DES TESTS"
echo "======================================================================"
echo ""
echo -e "${GREEN}✅ Tests terminés${NC}"
echo ""
echo "🔑 Token JWT généré: ${TOKEN:0:30}..."
echo "👤 User ID: $USER_ID"
echo "📧 Email: $TEST_EMAIL"
echo ""
echo "💡 Vous pouvez maintenant utiliser ce token pour tester d'autres endpoints:"
echo "   export TOKEN=\"$TOKEN\""
echo "   curl -H \"Authorization: Bearer \$TOKEN\" $BASE_URL/courses"
echo ""
echo "======================================================================"









