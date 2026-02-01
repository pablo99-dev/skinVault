from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render
from django.contrib import messages
# ======================
# Inscription
# ======================
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Vérifie que les mots de passe correspondent
        if password1 != password2:
            return render(request, "shop/signup.html", {
                "error": "Les mots de passe ne correspondent pas"
            })

        # Vérifie si le nom d'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            return render(request, "shop/signup.html", {
                "error": "Ce nom d'utilisateur est déjà utilisé"
            })

        # Crée l'utilisateur
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Redirige vers la page de connexion
        return redirect("login")
    else:
        # GET : afficher le formulaire
        return render(request, "shop/signup.html")

# ======================
# Connexion
# ======================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            # renvoyer le formulaire avec un message d'erreur
            return render(request, "shop/login.html", {
                "error": "Nom d'utilisateur ou mot de passe incorrect"
            })

    # GET : afficher le formulaire
    return render(request, "shop/login.html")

# ======================
# Dashboard (page après connexion)
# ======================
@login_required
def dashboard(request):
    categories = [
        'Knife', 'Rifle', 'SMG', 'Sniper', 'Pistol',
        'Shotgun', 'Machine Gun', 'Agent', 'Sticker'
    ]

    dashboard_data = {}

    with connection.cursor() as cursor:
        for category in categories:
            cursor.execute("""
                SELECT s.id, s.name, w.name, s.image_url, s.max_price
                FROM skin s
                JOIN weapon w ON s.weapon_id = w.id
                JOIN weapon_category c ON w.category_id = c.id
                WHERE c.name = %s
                ORDER BY w.name, s.name
            """, [category])

            rows = cursor.fetchall()

            skins_list = [
                {
                    'skin_id': row[0],
                    'skin_name': row[1],
                    'weapon_name': row[2],
                    'image': row[3],
                    'price': row[4],
                }
                for row in rows
            ]

            # Limiter à 6 skins par catégorie
            dashboard_data[category] = skins_list[:6]

    return render(request, 'shop/dashboard.html', {
        'dashboard_data': dashboard_data
    })



#def weapon_detail_by_name(request, weapon_name):
#    return render(request, 'shop/weapons.html', {'weapon_name': weapon_name})

#
#def weapon_detail_by_name(request, weapon_name):
#    # Données simulées
#    skins = [
#        {'name': 'Karambit Fade', 'price': 250, 'image': '/static/shop/images/logo.jpg'},
#        {'name': 'Karambit Doppler', 'price': 200, 'image': '/static/shop/images/logo.jpg'},
#        {'name': 'Karambit Marble', 'price': 180, 'image': '/static/shop/images/logo.jpg'},
#        {'name': 'Karambit Tiger', 'price': 150, 'image': '/static/shop/images/logo.jpg'},
#        {'name': 'Karambit Tiger', 'price': 150, 'image': '/static/shop/images/logo.jpg'},
#        {'name': 'Karambit Tiger', 'price': 150, 'image': '/static/shop/images/logo.jpg'},
#        {'name': 'Karambit Tiger', 'price': 150, 'image': '/static/shop/images/logo.jpg'},
#        {'name': 'Karambit Tiger', 'price': 150, 'image': '/static/shop/images/logo.jpg'},
#    ]
#
#    return render(request, 'shop/weapons.html', {
#        'weapon_name': weapon_name,
#        'skins': skins
#    })

# on pourra l'utiliser une fois on a bein definie la bdd
# Mapping URL -> nom exact dans la base
def weapon_detail_by_name(request, weapon_name):
    
    with connection.cursor() as cursor:
        # On récupère l'ID de l'arme et ses skins
        cursor.execute("""
            SELECT s.id, s.name, s.image_url, s.max_price
            FROM skin s
            JOIN weapon w ON s.weapon_id = w.id
            WHERE w.name = %s
            ORDER BY s.name;
        """, [weapon_name])
        skins_data = cursor.fetchall()

    # Conversion en dictionnaires pour le template
    skins = [
        {'skin_id' : row[0] , 'name': row[1], 'image': row[2], 'price': row[3]}
        for row in skins_data
    ]

    message = None
    if not skins:
        message = "Aucun skin disponible pour cette arme."

    return render(request, 'shop/weapons.html', {
        'weapon_name': weapon_name,
        'skins': skins,
        'message': message,
    })

@login_required
def favorites_view(request):
    user_id = request.user.id

    # Récupérer les skin_id favoris
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT skin_id
            FROM user_favorite
            WHERE user_id = %s
        """, [user_id])
        liked_skin_ids = [row[0] for row in cursor.fetchall()]

    # Vérifier si aucun favori
    if not liked_skin_ids:
        liked_skins = []
        message = "Vous n'avez aucun skin favori."
    else:
        message = None
        #  Récupérer les infos de ces skins
        with connection.cursor() as cursor:
            placeholders = ','.join(['%s'] * len(liked_skin_ids))
            query = f"""
                SELECT id, name, image_url, max_price
                FROM skin
                WHERE id IN ({placeholders}) 
                ORDER BY name
                """
            cursor.execute(query, liked_skin_ids)
            skins_data = cursor.fetchall() # recuperer les info du skins

        liked_skins = [
            {'skin_id': row[0], 'name': row[1], 'image': row[2], 'price': row[3]}
            for row in skins_data
        ]

    return render(request, 'shop/favorites.html', {
        'skins': liked_skins,
        'message': message,
    })


@login_required
def add_favorite(request):
    if request.method != "POST":
        return redirect("dashboard")

    user_id = request.user.id
    skin_id = request.POST.get("skin_id")

    if not skin_id:
        return redirect(request.POST.get("next", "/"))

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 1 FROM user_favorite
            WHERE user_id = %s AND skin_id = %s
        """, [user_id, skin_id])
        exists = cursor.fetchone()

        if exists:
            cursor.execute("""
                DELETE FROM user_favorite
                WHERE user_id = %s AND skin_id = %s
            """, [user_id, skin_id])
        else:
            cursor.execute("""
                INSERT INTO user_favorite (user_id, skin_id)
                VALUES (%s, %s)
            """, [user_id, skin_id])

    return redirect(request.POST.get("next", "/"))




@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
