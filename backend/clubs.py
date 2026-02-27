import psycopg
from flask import jsonify, request, g
from db import get_conn
from auth import token_required

# ---------------------------------------------------------------------------
# CLUBS
# ---------------------------------------------------------------------------

def show_clubs():
    """Show the list of clubs."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT c.id,
                               c.name,
                               c.city,
                               ARRAY_AGG(DISTINCT s.name) AS sports
                        FROM clubs c
                                 LEFT JOIN ladders l ON l.club_id = c.id
                                 LEFT JOIN sports s ON s.id = l.sport_id
                        GROUP BY c.id, c.name, c.city
                        ORDER BY c.name
                        """)
            rows = cur.fetchall()
    clubs = []
    for row in rows:
        sports = []
        for sport in row[3]:
            if sport is not None:
                sports.append(sport)
        clubs.append({
            'id': row[0],
            'name': row[1],
            'city': row[2],
            'sports': sports
        })
    return {"success": True, "clubs": clubs}
def join_club(user_id,club_id):
    "User can join a club."
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT club_id FROM members WHERE user_id = %s
                        """, (user_id,))
            exists = cur.fetchone()
            if exists:
                return {"success": False, "error": "You are already a member of a club!"}
            cur.execute("""
                        SELECT id
                        FROM clubs
                        WHERE id = %s
                        """, (club_id,))
            NotFound = cur.fetchone()
            if NotFound is None:
                return {"success": False, "error": "Club not found"}
            cur.execute("""
                        INSERT INTO members (user_id, club_id)
                        VALUES (%s, %s)
                        """, (user_id, club_id))
        conn.commit()
    return {"success": True, "message": "Successfully joined the club!"}
def leave_club(user_id):
    "User can leave a club."
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT club_id
                        FROM members
                        WHERE user_id = %s
                        """, (user_id,))
            exists = cur.fetchone()
            if exists is None:
                return {"success": False, "error": "You are not a member of a club!"}
            cur.execute("""
                        DELETE
                        FROM members
                        WHERE user_id = %s
                        """, (user_id,))
        conn.commit()
    return {"success": True, "message": "Successfully leave the club!"}