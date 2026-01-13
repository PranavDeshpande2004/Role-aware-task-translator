def detect_roles(matches):
    roles = []

    # Always take top 2–3 roles
    for m in matches[:3]:
        roles.append(m.metadata)

    return roles
