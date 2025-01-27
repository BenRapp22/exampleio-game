import constants

def applyCollisions(players, bullets):
    destroyedBullets = []

    for i in range(len(bullets)):
        for j in range(len(players)):
            bullet = bullets[i]
            player = players[i]

            if (bullet.parentID != player.id) and (player.distanceTo(bullet) <= constants.PLAYER_RADIUS+constants.BULLET_RADIUS):
                destroyedBullets.append(bullet)
                player.takeBulletDamage()
                break

    return destroyedBullets    
