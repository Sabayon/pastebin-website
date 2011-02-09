var Openmoomenu = new Class ({
	Implements : Options,
 
	options : {
		delay: 400,
		animate: {
			props: ['opacity', 'width', 'height'],
			options: {
				duration:500,
				fps: 100,
				transition: 'sine:out'
			}
		}
	},
 
	initialize: function(container, options) {
		this.setOptions(options);
		this.container = document.getElement(container);
		this.titles = this.container.getChildren(); 
		this.open = '';
		this.titles.each(function(title){
			if (title.getElement('ul')) {
				title.store('w',title.getElement('ul').getCoordinates(title).width);
				title.store('h', title.getElement('ul').getCoordinates(title).height);
				title.addEvent('mouseenter',function(title){
					$clear(this.remove_d);
					if (!title.hasClass('sfHover')) {
						if (this.open != ''){
							if (this.open.getElement('ul'))
								this.open.removeClass('sfHover'); 
							this.open = '';
						}
						this.menu = title.getElement('ul');
						this.open = title;
						this.transitions = {};
						this.options.animate.props.each(function (prop) {
							this.menu.setStyle(prop,0);
							if (prop == 'opacity')
								this.transitions.opacity = 1; 
							if (prop == 'width')
								this.transitions.width = title.retrieve('w'); 
							if (prop == 'height')
								this.transitions.height = title.retrieve('h'); 
						},this); 
						title.addClass('sfHover');
						this.menu.set('morph',this.options.animate.options);
						this.menu.get('morph').start(this.transitions);
					}
				}.bind(this,title));
 
				title.addEvent('mouseleave',function(title){
					this.remove_d = (function(){title.removeClass('sfHover'); this.open = '';}).delay(this.options.delay);
				}.bind(this,title)); 
			}
			else {
				title.addClass('');
				title.addEvent('mouseenter',function(title){
					$clear(this.remove_d);
					if (this.open != title) {
						if (this.open != ''){
							if (this.open.getElement('ul'))
								this.open.removeClass('sfHover'); 
							this.open = '';
						}
					}
					this.open = title;
				}.bind(this,title));
			}
		},this);
 
	}
});