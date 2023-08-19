import json
import urllib.request


class PIRIAPI_w20:
    mainEndponit = "https://core.pirichain.com/"
    testEndponit = "https://testnet.pirichain.com/"
    endpoint = ""

    def __init__(self, main):
        if main == True:
            self.endpoint = self.mainEndponit
        else:
            self.endpoint = self.testEndponit

    def sendHttpPostJson(self, url, data):
        try:
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json')
            req.add_header(
                'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47')
            req.add_header('Content-Length', str(len(data)))
            response = urllib.request.urlopen(
                req, data.encode('utf-8'), timeout=60)
            content = response.read().decode()
            return content
        except:
            raise

    def createNewAddress(self, language="english", commercial=False):
        data = {"language": language, "isCommercial": str(commercial)}
        return self.sendHttpPostJson(self.endpoint+"createNewAddress", json.dumps(data))

    def rescuePrivateKey(self, words, language="english"):
        if (len(words) < 8):
            raise
        data = {"words": words, "language": language}
        return self.sendHttpPostJson(self.endpoint+"rescuePrivateKey", json.dumps(data))

    def getMnemonic(self, privateKey, language="english"):
        if (len(privateKey) < 8):
            raise
        data = {"privateKey": privateKey, "language": language}
        return self.sendHttpPostJson(self.endpoint+"getMnemonic", json.dumps(data))

    def getBalance(self, address, assetID="-1"):
        if (len(address) < 8):
            raise
        data = {"address": address, "assetID": assetID}
        return self.sendHttpPostJson(self.endpoint+"getBalance", json.dumps(data))

    def getBalanceList(self, address):
        if (len(address) < 8):
            raise
        data = {"address": address}
        return self.sendHttpPostJson(self.endpoint+"getBalanceList", json.dumps(data))

    def getToken(self, assetID="-1"):
        data = {"assetID": assetID}
        return self.sendHttpPostJson(self.endpoint+"getToken", json.dumps(data))

    def listTokens(self, skip="0", limit='10'):
        data = {"skip": skip, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"listTokens", json.dumps(data))

    def sendToken(self, address, privateKey, to, amount, assetID="-1"):
        if ((len(address) < 8) and (len(privateKey) < 8) and (len(to) < 8)):
            raise
        data = {"address": address, "privateKey": privateKey,
                "to": to, "amount": amount, "assetID": assetID}
        return self.sendHttpPostJson(self.endpoint+"sendToken", json.dumps(data))

    def createToken(self, creatorAddress, privateKey, tokenName, tokenSymbol, totalSupply, logo, decimals, description, webSite, socialMediaFacebookURL, socialMediaTwitterURL, socialMediaMediumURL, socialMediaYoutubeURL, socialMediaRedditURL, socialMediaBitcoinTalkURL, socialMediaInstagramURL, mailAddress, companyAddress, sector, hasAirdrop, hasStake):
        data = {"creatorAddress": creatorAddress, "privateKey": privateKey, "tokenName": tokenName, "tokenSymbol": tokenSymbol, "totalSupply": totalSupply, "logo": logo, "decimals": decimals, "description": description, "webSite": webSite, "socialMediaFacebookURL": socialMediaFacebookURL, "socialMediaTwitterURL": socialMediaTwitterURL, "socialMediaMediumURL": socialMediaMediumURL,
                "socialMediaYoutubeURL": socialMediaYoutubeURL, "socialMediaRedditURL": socialMediaRedditURL, "socialMediaBitcoinTalkURL": socialMediaBitcoinTalkURL, "socialMediaInstagramURL": socialMediaInstagramURL, "mailAddress": mailAddress, "companyAddress": companyAddress, "sector": sector, "hasAirdrop": str(hasAirdrop), "hasStake": str(hasStake)}
        return self.sendHttpPostJson(self.endpoint+"createToken", json.dumps(data))

    def getScenario(self, address):
        data = {"address": address}
        return self.sendHttpPostJson(self.endpoint+"getScenario", json.dumps(data))

    def createScenario(self, address, privateKey, scenarioText, name, description, tags):
        if (len(address) < 8):
            raise
        data = {"address": address, "privateKey": privateKey, "scenarioText": scenarioText,
                "name": name, "description": description, "tags": tags}
        return self.sendHttpPostJson(self.endpoint+"createScenario", json.dumps(data))

    def listMyScenarios(self, ownerAddress):
        if (len(ownerAddress) < 8):
            raise
        data = {"ownerAddress": ownerAddress}
        return self.sendHttpPostJson(self.endpoint+"listMyScenarios", json.dumps(data))

    def listScenarios(self, skip="0", limit='10'):
        data = {"skip": skip, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"listScenarios", json.dumps(data))

    def executeScenario(self, scenarioAddress, address, privateKey, method, params):
        # params = ["Data1", "Data2"]
        data = {"scenarioAddress": scenarioAddress, "address": address,
                "privateKey": privateKey, "method": method, "params": params}
        return self.sendHttpPostJson(self.endpoint+"executeScenario", json.dumps(data))

    def previewScenario(self, scenarioText, address, privateKey, method, params):
        # params = ["Data1", "Data2"]
        data = {"scenarioText": scenarioText, "address": address,
                "privateKey": privateKey, "method": method, "params": params}
        return self.sendHttpPostJson(self.endpoint+"previewScenario", json.dumps(data))

    def listTransactions(self, skip="0", limit='50'):
        data = {"skip": skip, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"listTransactions", json.dumps(data))

    def listPoolTransactions(self):
        data = {}
        return self.sendHttpPostJson(self.endpoint+"listPoolTransactions", json.dumps(data))

    def listTransactionsByAssetID(self, assetID, skip="0", limit='10'):
        data = {"skip": skip, "limit": limit, "assetID": assetID}
        return self.sendHttpPostJson(self.endpoint+"listTransactionsByAssetID", json.dumps(data))

    def listTransactionsByAddr(self, address, skip="0", limit='10'):
        data = {"skip": skip, "limit": limit, "address": address}
        return self.sendHttpPostJson(self.endpoint+"listTransactionsByAddr", json.dumps(data))

    def getTransaction(self, tx):
        if (len(tx) < 8):
            raise
        data = {"tx": tx}
        return self.sendHttpPostJson(self.endpoint+"getTransaction", json.dumps(data))

    def getPoolTransaction(self, tx):
        if (len(tx) < 8):
            raise
        data = {"tx": tx}
        return self.sendHttpPostJson(self.endpoint+"getPoolTransaction", json.dumps(data))

    def getDetailsOfAddress(self, address):
        if (len(address) < 8):
            raise
        data = {"address": address}
        return self.sendHttpPostJson(self.endpoint+"getDetailsOfAddress", json.dumps(data))

    def getBlocks(self, skip="0", limit='10'):
        data = {"skip": skip, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"getBlocks", json.dumps(data))

    def getBlocksDesc(self, skip="0", limit='10'):
        data = {"skip": skip, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"getBlocksDesc", json.dumps(data))

    def getLastBlocks(self, limit='10'):
        data = {"limit": limit}
        return self.sendHttpPostJson(self.endpoint+"getLastBlocks", json.dumps(data))

    def getOnlyBlocks(self, skip="0", limit='10'):
        data = {"skip": skip, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"getOnlyBlocks", json.dumps(data))

    def getBlock(self, blockNumber):
        if (len(blockNumber) < 1):
            raise
        data = {"blockNumber": blockNumber}
        return self.sendHttpPostJson(self.endpoint+"getBlock", json.dumps(data))

    def decrypt(self, customID, privateKey, receiptPub):
        data = {"customID": customID,
                "privateKey": privateKey, "receiptPub": receiptPub}
        return self.sendHttpPostJson(self.endpoint+"decrypt", json.dumps(data))

    def pushData(self, address, privateKey, to, customData, inPubKey):
        if (len(address) < 8):
            raise
        data = {"address": address, "privateKey": privateKey,
                "to": to, "customData": customData, "inPubKey": inPubKey}
        return self.sendHttpPostJson(self.endpoint+"pushData", json.dumps(data))

    def pushDataList(self, address, privateKey, to, customData):
        if (len(address) < 8):
            raise
        data = {"address": address, "privateKey": privateKey,
                "to": to, "customData": customData}
        return self.sendHttpPostJson(self.endpoint+"pushData", json.dumps(data))

    def listData(self, skip="0", limit='10'):
        data = {"skip": skip, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"listData", json.dumps(data))

    def listDataByAddress(self, address, skip="0", limit='10'):
        if (len(address) < 8):
            raise
        data = {"address": address, "skip": skip, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"listDataByAddress", json.dumps(data))

    def getAddressListByAsset(self, assetID='-1', start="0", limit='10'):
        data = {"assetID": assetID, "start": start, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"getAddressListByAsset", json.dumps(data))

    def isValidAddress(self, address):
        if (len(address) < 8):
            raise
        data = {"address": address}
        return self.sendHttpPostJson(self.endpoint+"isValidAddress", json.dumps(data))

    def search(self, value):
        if (len(value) < 1):
            raise
        data = {"value": value}
        return self.sendHttpPostJson(self.endpoint+"search", json.dumps(data))

    def listMyDelegation(self, delegationAddress, delegationPrivateKey):
        data = {"delegationAddress": delegationAddress,
                "delegationPrivateKey": delegationPrivateKey}
        return self.sendHttpPostJson(self.endpoint+"listMyDelegation", json.dumps(data))

    def unFreezeCoin(self, delegationAddress, delegationPrivateKey, nodeAddress, txHash):
        data = {"delegationAddress": delegationAddress, "delegationPrivateKey":
                delegationPrivateKey, "nodeAddress": nodeAddress, "txHash": txHash}
        return self.sendHttpPostJson(self.endpoint+"unFreezeCoin", json.dumps(data))

    def freezeCoin(self, delegationAddress, delegationPrivateKey, duptyAddress, amount):
        data = {"delegationAddress": delegationAddress, "delegationPrivateKey":
                delegationPrivateKey, "duptyAddress": duptyAddress, "amount": amount}
        return self.sendHttpPostJson(self.endpoint+"freezeCoin", json.dumps(data))

    def joinAsDeputy(self, address, privateKey, alias):
        data = {"address": address, "privateKey": privateKey, "alias": alias}
        return self.sendHttpPostJson(self.endpoint+"joinAsDeputy", json.dumps(data))

    def checkDeputy(self, address):
        if (len(address) < 8):
            raise
        data = {"address": address}
        return self.sendHttpPostJson(self.endpoint+"checkDeputy", json.dumps(data))

    def listDeputies(self):
        data = {}
        return self.sendHttpPostJson(self.endpoint+"listDeputies", json.dumps(data))

    def getMyRewardQuantity(self, base58, privateKey):
        if (len(base58) < 8):
            raise
        data = {"base58": base58, "privateKey": privateKey}
        return self.sendHttpPostJson(self.endpoint+"getMyRewardQuantity", json.dumps(data))

    def createAddressForBuyPiri(self, type):
        data = {"type": type}
        return self.sendHttpPostJson(self.endpoint+"createAddressForBuyPiri", json.dumps(data))

    def getBalanceForBuyPiri(self, type, address, piriAddress):
        data = {"type": type, "address": address, "piriAddress": piriAddress}
        return self.sendHttpPostJson(self.endpoint+"getBalanceForBuyPiri", json.dumps(data))

    def getPiriPrice(self, type='busd'):
        data = {"type": type}
        return self.sendHttpPostJson(self.endpoint+"getPiriPrice", json.dumps(data))

    def getRichList(self, assetID='-1', skip="0", limit='10'):
        data = {"assetID": assetID, "skip": skip, "limit": limit}
        return self.sendHttpPostJson(self.endpoint+"getRichList", json.dumps(data))

    def getDetailStats(self, assetID='-1'):
        data = {"assetID": assetID}
        return self.sendHttpPostJson(self.endpoint+"getDetailStats", json.dumps(data))

    def getStats(self):
        data = {}
        return self.sendHttpPostJson(self.endpoint+"getStats", json.dumps(data))

    def listDelegationTopN(self):
        data = {}
        return self.sendHttpPostJson(self.endpoint+"listDelegationTopN", json.dumps(data))

    def getCirculation(self):
        data = {}
        return self.sendHttpPostJson(self.endpoint+"getCirculation", json.dumps(data))
