## What are pumps and dumps?

Pump and dump refers to the process of a bad actor artificially raising the price (the pump)
and subsequent selling to make a large profit (dump). Since Cryptocurrencies don't have regulations, such things are more common here.

![Untitled](https://user-images.githubusercontent.com/55044774/119353619-bd439e00-bcc0-11eb-9291-64b0208e0fce.png)

The above image is just for reference. The actual pump and Dump lasts for about a minute or two. And the Volume of the pump is determined by how many people buy that particular coin which is mostly influenced by the number of people in the telegram/discord groups that the owners operate and the number of people who FOMO into the coin, while that pump and dump are at the action.

Below is a real pump and dump organised by a telegram group with over 500k members.

![pumpanddump](https://user-images.githubusercontent.com/55044774/119353649-c3d21580-bcc0-11eb-84f7-f06d850aa235.png)

## Can people make profit from such schemes ?

Maybe, if you are fast enough to buy the announced coin at fast as you can. But why use humans when we have computers for such boring stuff. So I tried to Automate this buying and selling of the announced coin a fast as possible. How? 

1. Use Binance APIs to build a python based CLI program where you can feed in essential info ( like amount, take profit, stop loss, etc .. ) and it does that for you.
2. To make it even faster, I integrated telegram chat's message capture. So as soon as the Bot is open and the coin is announced ( usually they always prepend the coin name with a dollar sign, like $BTC, $ETH ) . the bot will automatically capture the correct coin name and place an immediate market buy order.

## Some usage stats

1. 40 + users registered and used the bot.
2. 3 users took the premium subscription. ( $25 )

# Future Improvements using ML

As we have all the market data from the major crypto exchanges, we can train an ML model to predict the coin which is going to be pumped based on previous market patterns before the pump( the whales buying before the pump, etc. . )

With this, we can stop these malpractices from happening altogether as the exchanges can take action against those who indulge in the pump and dump.

Inspired from [http://cs229.stanford.edu/proj2017/final-reports/5231579.pdf](http://cs229.stanford.edu/proj2017/final-reports/5231579.pdf)
