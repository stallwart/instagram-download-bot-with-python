import os, shutil, sys, instaloader
from prettytable import PrettyTable
instagramBot = instaloader.Instaloader(quiet = True)
# https://github.com/xsoulfire
# Lisanslı Projedir. Kopyalanması veya Ticari Olarak işlenmesi halinde gerekli işlemler için müracaat edilecektir.
def auth():
    userName = input("Instagram Kullanıcı Adını Gir: ")
    try:
        instagramBot.load_session_from_file(userName)
    except:
        try:
            os.system("instaloader -l {0}".format(userName))
            instagramBot.load_session_from_file(userName)
        except:
            instagramBot.login(userName,input("Şifreni Gir: "))
            instagramBot.save_session_to_file()
    print("{0} Giriş Yapıldı.".format(userName))
def main():
    auth()
    while True:
        print("Soulfire Is Always Here")
        myTable = PrettyTable(["Seçenekler","Görev"])
        myTable.add_row(["1", "Kullanıcı Adını Girdiğin Hesabın Profil Fotoğrafını İndir!"])
        myTable.add_row(["2", "Kullanıcı Adını Girdiğin Hesabın Tüm Gönderilerini İndir!"])
        myTable.add_row(["3", "Hashtag'deki Tüm Fotoğrafları İndir!"])
        print(myTable)
        query = input("Görev Seçiniz")
        if query == "1":
            currentPath = os.getcwd()
            username = input("PP'sini İndirmek İstediğin Hesabın Kullanıcı Adını Yaz: ")
            instagramBot.download_profile(username, profile_pic_only = True)
            for file in os.listdir(username):
                if ".jpg" in file:
                    shutil.move("{0}/{1}".format(username,file),currentPath)
            shutil.rmtree(username)
            print("'{0}' Profil Fotoğrafı İndirildi.".format(username))
        elif query == "2":
            currentPath = os.getcwd()
            username = input("İndirmek için kullanıcı adı gir: ")
            try : 
                profile = instaloader.Profile.from_username(instagramBot.context, username)
            except:
                print("Username Not Found.")
            if os.path.exists(username) is False:
                os.mkdir(username)
            os.chdir(username)
            if os.path.exists("Videos") is False:
                os.mkdir("Videos")
            posts = profile.get_posts()
            print("İndiriliyor... durdurmak için Ctrl + C yapın. Kullanıcı Adı Klasörünü Açmayın.")
            for index, post in enumerate(posts):
                try:
                    instagramBot.download_post(post, target = index)
                except KeyboardInterrupt:
                    print("İndiriciden Çıkıldı.")
                    break
            for folder in os.listdir():
                if "." not in folder:
                    for item in os.listdir(folder):
                        if ".jpg" in item:
                            shutil.move(folder+"/"+item, "{0}/{1}".format(currentPath, username))
                        elif ".mp4" in item:
                            try:
                                shutil.move(folder+"/"+item, "{0}/{1}/Videos".format(currentPath, username))
                            except:
                                continue
                    shutil.rmtree(folder)
            print("{} Klasör Oluşturuldu.".format(username))
        elif query == "3":
            try:
                instaloader.Instaloader(download_videos=False, save_metadata=False, post_metadata_txt_pattern='').download_hashtag(input("Hashtag Giriniz: "), max_count=20)
            except KeyboardInterrupt:
                print("İndiriciden Çıkıldı")
if __name__ == "__main__":
    main()
