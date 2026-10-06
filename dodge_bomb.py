import os
import sys
import pygame as pg
import random as ran
import time


WIDTH, HEIGHT = 1100, 650  # 背景画像の縦幅、横幅
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5), 
    pg.K_LEFT:(-5,0), 
    pg.K_RIGHT:(5,0)
    }

os.chdir(os.path.dirname(os.path.abspath(__file__)))



# 画面内外判定関数
def check_bound(rect: pg.rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRect or 爆弾Rect 
    戻り値：タプル(横方向判定結果・縦方向判定結果)
    (True：画面内/False：画面外）
    """
    y_jujge, x_jujge = True , True

    if (rect.top<0) or (rect.bottom>HEIGHT):
        y_jujge = False
    
    if (rect.left<0) or (rect.right>WIDTH):
        x_jujge = False
    
    return x_jujge, y_jujge

# 追加機能1
# ゲームオーバー画面を表示する関数
def gameover(screen: pg.Surface) -> None:
    # 黒画面
    gameover_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(gameover_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    gameover_img.set_alpha(200)

    # テキスト描画
    fonto = pg.font.Font(None,100)
    txt = fonto.render("Game Over",True,(255,255,255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH//2,HEIGHT//2)
    gameover_img.blit(txt,txt_rct)

    # こうかとん描画
    clykk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1)
    clykk_rct1 = clykk_img.get_rect()
    clykk_rct2 = clykk_img.get_rect()
    clykk_rct1.center = (WIDTH//4,HEIGHT//2)
    clykk_rct2.center = (WIDTH//4*3,HEIGHT//2)
    gameover_img.blit(clykk_img,clykk_rct1)
    gameover_img.blit(clykk_img,clykk_rct2)

    # 画面更新
    screen.blit(gameover_img,[0,0])
    pg.display.update()
    time.sleep(3)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()

    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = ran.randint(0,WIDTH), ran.randint(0,HEIGHT)



    clock = pg.time.Clock()
    tmr = 0
    vx,vy = 5, 5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾が重なったら終了
            gameover(screen=screen)
            print("ゲームオーバー!")
            return 0

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)

        # こうかとんの画面外挙動
        if(check_bound(kk_rct) != (True,True)): 
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx,vy)

        bb_x, bb_y = check_bound(bb_rct)
        # 爆弾の画面外挙動
        if bb_x != True:  # 横にはみ出た場合
            vx *= -1
        if bb_y != True:  # 縦にはみ出た場合
            vy *= -1

        screen.blit(bb_img, bb_rct)


        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
