from __future__ import unicode_literals
#-*-coding:utf8 -*-


from bs4 import BeautifulSoup


def extract_trip(content):
    content = BeautifulSoup(content,"html5lib")
    imgs = content.find_all("img")
    return imgs[0]['src']





if __name__ == "__main__":
    content = """
    本来中秋想回家的，应该回去看看老爸，祭奠一下老妈。但我最近的压力很大，就想着到海边放松一下。于是乎，我们订好了去烟台的票。

有很多人不理解，为什么会选择烟台呢？之所以选择烟台，是因为我出去的目的是散心，只想在海边坐一坐，听听海浪声。我这个人一直都是对海情有独钟，我认为在海边我可以暂时忘却所有的不愉快和烦恼，那种感觉真的很美妙。

我们并没有选择直达烟台，而是从青岛转车，这么做的原因是我们想在青岛吃一顿念念不忘的海鲜。去年我们去青岛拍婚纱照，媳妇的同事请我们吃了一家叫田横渔村的海鲜。我不是想吃海鲜本身，而是特别喜欢他们家的卤
    <p type=hidden id="trip_date">2017-03-06</p>
    <img src='http://dailyblog-dailyblog.stor.sinaapp.com/170043430004682103.jpg' />
    <img src='http://dailyblog-dailyblog.stor.sinaapp.com/170043430004682103.jpg' />
    <img id="tripimg" src='http://dailyblog-dailyblog.stor.sinaapp.com/170043430004682103.jpg' />
    <p id="tripdate" title='2017-10-1'></p>
    """
    print  extract_trip(content)