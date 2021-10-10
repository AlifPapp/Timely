    # tdatareplace
    @commands.command()
    async def datareplace(self, ctx):
        await ctx.send(f"Initiated data replace")
        
        cluster = self.client.mongodb["Currency"]["Main"]
        list_of_users = cluster.find().sort("savings", -1)
        cycle_int = 0
        for x in list_of_users:
            cycle_int = cycle_int + 1
            cluster.replace_one({"id":x["id"]},{"id": x["id"], "savings": x["savings"],"lifespan": x["lifespan"],"luck": 0, 
                                 "commands_used": 0, "stolen": 0,
                                 "daily": x["daily"], "weekly": x["weekly"], "monthly": x["monthly"],
                                 "pray": 0})
        
        await ctx.send(f"Finished converting {cycle_int} accounts")
    
    # tadddata
    @commands.command()
    async def adddata(self, ctx):
        cluster = self.client.mongodb["Counting"]["Emojis"]

        data = {"Name": "blob",
                 "Emoji_0": "<:number_blob_0:884691502347976745>",
                 "Emoji_1": "<:number_blob_1:884691531641008198>",
                 "Emoji_2": "<:number_blob_2:884691557146562570>",
                 "Emoji_3": "<:number_blob_3:884691582173999114>",
                 "Emoji_4": "<:number_blob_4:884691603762073640>",
                 "Emoji_5": "<:number_blob_5:884691625002041374>",
                 "Emoji_6": "<:number_blob_6:884691650037841980>",
                 "Emoji_7": "<:number_blob_7:884691669239361546>",
                 "Emoji_8": "<:number_blob_8:884691687778156574>",
                 "Emoji_9": "<:number_blob_9:884691707495579659>",
                 "Emoji_gif": "<a:number_blob_gif:884744128422879233>"}
        cluster.insert_one(data)

        await ctx.send(f"Inserted data")

    # tadddata2
    @commands.command()
    async def adddata2(self, ctx):
        cluster = self.client.mongodb["Counting"]["Emojis"]
        emojis = cluster.find()
        data = {}
        for x in emojis:
            data[x["Name"]] = {}
            i = 0
            while i < 10:
                data[x["Name"]][f"Emoji_{i}"] = x[f"Emoji_{i}"]
                i = i + 1
            data[x["Name"]]["Emoji_gif"] = x["Emoji_gif"]
        
        with open("count_emojis.json","w") as f: 
            json.dump(data, f)

        await ctx.send(f"Inserted data file")