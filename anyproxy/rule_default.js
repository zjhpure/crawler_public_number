function sendToRedis(x_wechat_key, x_wechat_uin, user_agent, cookie, url) {
    var redis = require("redis");
    client = redis.createClient(6379, 'localhost', {});
    client.auth('123456');
    client.on("error", function (err) {
        console.log("Error " + err);
    });
    var now = Math.round(new Date().getTime() / 1000)
    console.log(now);
    client.rpush('crawl_pub_click', x_wechat_key + '&&' + x_wechat_uin + '&&' + user_agent + '&&' + cookie + '&&' + now + '&&' + url, redis.print)
    client.quit();
};

'use strict';

module.exports = {

    summary: 'the default rule for AnyProxy',

    /**
     *
     *
     * @param {object} requestDetail
     * @param {string} requestDetail.protocol
     * @param {object} requestDetail.requestOptions
     * @param {object} requestDetail.requestData
     * @param {object} requestDetail.response
     * @param {number} requestDetail.response.statusCode
     * @param {object} requestDetail.response.header
     * @param {buffer} requestDetail.response.body
     * @returns
     */
    *beforeSendRequest(requestDetail) {
        return null;
    },

    /**
     *
     *
     * @param {object} requestDetail
     * @param {object} responseDetail
     */
    *beforeSendResponse(requestDetail, responseDetail) {
        var tempStr = "mp.weixin.qq.com/mp/profile_ext?action=home";
        var res = requestDetail.url.indexOf(tempStr)
        if (res > 0) {
            var body = responseDetail.response.body
            var regu = "操作频繁，请稍后再试";
            if (body.indexOf(regu) >= 0) {
                console.log('微信操作频繁网页');
            } else {
                var data = requestDetail.requestOptions;
                sendToRedis(data.headers['x-wechat-key'], data.headers['x-wechat-uin'], data.headers['User-Agent'], data.headers['Cookie'], requestDetail.url)
                console.log(data);
            }
        }
        return null;
    },


    /**
     *
     *
     * @param {any} requestDetail
     * @returns
     */
    *beforeDealHttpsRequest(requestDetail) {
        return false;
    },

    /**
     *
     *
     * @param {any} requestDetail
     * @param {any} error
     * @returns
     */
    *onError(requestDetail, error) {
        return null;
    },


    /**
     *
     *
     * @param {any} requestDetail
     * @param {any} error
     * @returns
     */
    *onConnectError(requestDetail, error) {
        return null;
    },
};
