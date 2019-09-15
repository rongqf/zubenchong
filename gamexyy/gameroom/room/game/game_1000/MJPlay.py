#coding:utf8

import MJCard
import MJHandCard
import MJCardPile


MJ_CHI = 1
MJ_PENG = 2
MJ_GANG = 3

MJ_ACT_MOPAI = 1
MJ_ACT_CHUPAI = 2
MJ_ACT_CHIPAI = 3
MJ_ACT_PENGPAI = 4
MJ_ACT_GANGPAI = 5
MJ_ACT_GANTING = 6
MJ_ACT_GANHU = 7


class MJOpenCard:
    def __init__(self, cardtype, cards):
        self.cardtype = cardtype
        self.cards = cards

    def gettype(self):
        return self.cardtype

    def getcards(self):
        return self.cards

    def getlen(self):
        return len(self.cards)


class MJPlayer:
    def __init__(self):

        self.act = []
        self.handcard = MJHandCard.MJHandCard()
        self.opencards = []
        self.state = None

    def mopai(self, card):
        self.handcard.addcard(card.getcolor(), card.getpoint())
        return True

    def chupai(self,card):
        if self.handcard.getcardnum(card.getcolor(), card.getpoint()) > 0:
            self.handcard.delcard(card.getcolor(), card.getpoint())
            return True
        else:
            return False

    def iscanchiex(self, cards):
        #return self.handcard.iscanchi(card.getcolor(), card.getpoint())
        return self.handcard.iscanchiex(cards)


    def iscanchi(self, card):
        return self.handcard.iscanchi(card.getcolor(), card.getpoint())

    def iscanpeng(self, card):
        return self.handcard.iscanpeng(card.getcolor(), card.getpoint())

    def iscangang(self, card):
        return self.handcard.iscangang(card.getcolor(), card.getpoint())

    def iscanting(self, card):
        return self.handcard.iscanting()

    def iscanhuself(self):
        return self.handcard.iscanhuself()

    def iscanhu(self, card):
        return self.handcard.iscanhu(card.getcolor(), card.getpoint())

    def iscanbumo(self, action, card):
        tmp = {MJ_ACT_GANHU:self.iscanhu, MJ_ACT_GANGPAI:self.iscangang, MJ_ACT_PENGPAI:self.iscanpeng, MJ_ACT_CHIPAI:self.iscanchi}

        if action in tmp:
            if tmp[action](card):
                return True
        return False

    def chipai(self, args):
        cards = args
        if self.iscanchiex(cards):
            for x in cards[1:]:
                self.handcard.delcard(x.getcolor(), x.getpoint())
            self.opencards.append(MJOpenCard(MJ_PENG, cards))
           

    def pengpai(self, args):   
        card = args
        if self.iscanpeng(card):
            self.handcard.delcard(card.getcolor(), card.getpoint(), 2)
            self.opencards.append(MJOpenCard(MJ_PENG, [card] * 3))
            

    def gangpai(self, args):
        card = args
        if self.iscangang(card):
            self.handcard.delcard(card.getcolor(), card.getpoint(), 3)
            self.opencards.append(MJOpenCard(MJ_GANG, [card] * 4))
        

    def tingpai(self, args):
        if self.iscanting(args):
            pass

    def hupai(self, args):
        card = MJCard.MJCard.i2c(args)
        if self.iscanhu(card):
            pass
    
    def actcard(act, args):
        tmp = {
            MJ_ACT_MOPAI: self.mopai,
            MJ_ACT_CHUPAI: self.chupai,
            MJ_ACT_CHIPAI: self.chipai,
            MJ_ACT_PENGPAI: self.pengpai,
            MJ_ACT_GANGPAI: self.gangpai,
            MJ_ACT_GANTING: self.tingpai,
            MJ_ACT_GANHU: self.hupai
        }        

        
        if act in tmp:
            return tmp[act](args)