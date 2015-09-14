var File = Backbone.Model.extend({
});

var FileCollection = Backbone.Collection.extend({
	model: File,
    url: '',
    accessToken: '',
    
    // sync: function(method, model, options) {
    //     var that = this;
    //     var params = _.extend({
    //         type: 'GET',
    //         dataType: 'jsonp',
    //         url: that.url + that.accessToken,
    //         processData: false
    //     }, options);

    //     return $.ajax(params);
    // },

    parse: function(response) {
        return response.data;
    }
});

var FileView = Backbone.View.extend({
	tagname: "li",
    model: File,
	render:function(){
		this.$el.html('<li><img src="' + this.model.get("source") + '"/></li>');
        return this;
	}
});

var FileCollectionView = Backbone.View.extend({
    tagname: "li",
    model: FileCollection,
    render: function() {
        this.$el.html();
        
        var self = this;

        for(var i = 0; i < this.model.length; ++i) {
            var fileViewInstance = new FileView({model: this.model.at(i)});

            this.$el.append(fileViewInstance.$el); 
            fileViewInstance.render();         
        } 

         return this;
    }
});

var Folder = Backbone.Model.extend({
    
});

var FolderCollection = Backbone.Collection.extend({
    model: Folder,
    url: '',
    parse: function(response){
        return response;
    }
});

var FolderView = Backbone.View.extend({
	tagname: "li",
    model: FolderCollection,
	render:function(){
		this.$el.html('<li>' + this.model.get("name") + '</li>');
        return this;
	},
    events: {
        "click": "getPhotos"
    },
    getPhotos: function( event ){
        var fileCollectionInstance = new FileCollection();
    	fileCollectionInstance.url = 'https://graph.facebook.com/v2.3/' + this.model.get('item_id') + '/photos' + '?' + this.model.get('access_token');
        fileCollectionInstance.fetch({
        	success: _.bind(function(collection, response, options){
				var fileCollectionViewInstance = new FileCollectionView({el: $("#green"), model: this});
				fileCollectionViewInstance.render();
            }, fileCollectionInstance)
        });
		console.log('gettingphotosfrom' + this.model.get("name"));
    }
});

var FolderCollectionView = Backbone.View.extend({
    initialize: function() {
        console.log('sampleView has been created');
    },
     render: function() {
        this.$el.html();
        
        var self = this;

        for(var i = 0; i < this.model.length; ++i) {
            var folderViewInstance = new FolderView({model: this.model.at(i)});

            this.$el.append(folderViewInstance.$el); 
            folderViewInstance.render();          
        } 

         return this;
    }
});
