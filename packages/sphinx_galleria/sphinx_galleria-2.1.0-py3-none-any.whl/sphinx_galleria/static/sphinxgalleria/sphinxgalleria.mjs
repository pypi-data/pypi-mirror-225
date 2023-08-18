"use strict()";

export class SphinxGalleria {
    constructor(target, options, data) {
        var self = this;
        self.target = target;
        self.options = options;
        self.data = data;
        self.oneimage = self.data.length === 1;
        self.swipe_delay = 1500;
        self.touch_data = {
            id: -1,
            x: null,
            y: null,
            current_x: null,
            current_y: null,
            interval: null,
            swiped: false,
            noclick: false
        };

        self.node_target = null;
        self.node_figure = document.createElement('figure');
        self.button_modal = document.createElement('button');
        self.button_modal.setAttribute('aria-haspopup', 'dialog');
        self.button_modal.classList.add('button-modal');

        self.node_image = document.createElement('img');
        self.node_caption = document.createElement('figcaption');
        self.node_alt = document.createElement('p');
        self.node_alt.setAttribute('id', self.target+'-'+'alt');
        self.node_image.setAttribute('aria-labelledby', self.target+'-'+'alt');
        self.node_thumbnails = document.createElement('ul');
        self.node_thumbnails.classList.add('thumbnails');
        self.node_dialog = document.createElement('dialog');
        self.node_mask = document.createElement('div');
        self.node_mask.classList.add('mask');
        self.node_mask.hidden = true;
        self.node_mask.setAttribute('aria-hidden', true);
        var node_submask = document.createElement('div');
        node_submask.classList.add('submask');

        self.node_div_caption = document.createElement('div');
        self.node_div_caption.classList.add('caption');

        var figure_row = document.createElement('div');
        figure_row.classList.add('row');

        self.dialog_button_close_icon = document.createElement('button');
        self.dialog_button_close_icon.setAttribute('aria-label', self.options.label_close);

        self.dialog_image = document.createElement('img');
        self.dialog_image.setAttribute('aria-labelledby', self.target+'-'+'alt');

        self.dialog_title = document.createElement('h1');
        var dialog_header = document.createElement('header');
        var dialog_menu = document.createElement('menu');

        if(self.oneimage) {
            self.node_thumbnails.hidden = true;
            self.node_thumbnails.setAttribute('aria-hidden', true);
            self.node_thumbnails.style.display = 'none';
        } else {
            self.node_slider = document.createElement('input');
            self.node_slider.setAttribute('type', 'range');
            self.node_slider.setAttribute('min', 1);
            self.node_slider.setAttribute('max', self.data.length);
            self.node_slider.setAttribute('value', 1);

            self.button_prev = document.createElement('button');
            self.button_prev.classList.add('prev');
            self.button_prev.setAttribute('aria-label', self.options.label_prev);

            self.button_next = document.createElement('button');
            self.button_next.classList.add('next');
            self.button_next.setAttribute('aria-label', self.options.label_next);

            self.dialog_button_prev = document.createElement('button');
            self.dialog_button_prev.classList.add('prev');
            self.dialog_button_next = document.createElement('button');
            self.dialog_button_next.classList.add('next');
            self.dialog_button_prev.appendChild(document.createTextNode(self.options.label_prev));
            self.dialog_button_next.appendChild(document.createTextNode(self.options.label_next));

            figure_row.appendChild(self.button_prev);
            dialog_menu.appendChild(self.dialog_button_prev);
            dialog_menu.appendChild(self.dialog_button_next);
        }

        node_submask.appendChild(self.node_dialog);
        self.node_mask.appendChild(node_submask);

        figure_row.appendChild(self.button_modal);
        self.node_figure.appendChild(figure_row);

        self.node_div_caption.appendChild(self.node_caption);
        self.node_div_caption.appendChild(self.node_alt);
        self.button_modal.appendChild(self.node_image);
        self.node_figure.appendChild(self.node_div_caption);

        dialog_header.appendChild(self.dialog_title);
        dialog_header.appendChild(self.dialog_button_close_icon);
        self.node_dialog.appendChild(dialog_header);
        self.node_dialog.appendChild(self.dialog_image);
        self.node_dialog.appendChild(dialog_menu);

        if(!self.oneimage) {
            figure_row.appendChild(self.button_next);
        }
    }

    init() {
        var self = this;
        self.node_target = document.getElementById(self.target);
        if(self.options.no_transition || self.oneimage) {
            if(!self.node_target.classList.contains('no-transition')) {
                self.node_target.classList.add('no-transition');
            }
        }
        self.node_target.innerHTML = '';
        self.node_target.classList.add("sphinxgalleria-core");
        self.node_target.appendChild(self.node_figure);
        if(!self.oneimage) {
            self.node_target.appendChild(self.node_slider);
        }
        self.node_target.appendChild(self.node_thumbnails);
        self.node_target.appendChild(self.node_mask);

        var onmodal = function(ev) {
            if(self.touch_data.noclick) {
                self.touch_data.noclick = false;
                ev.preventDefault();
                return;
            }
            var key = ev.key;
            if(ev.type==='keypress' && key!==" " && key!=="Enter") {
                return;
            }
            ev.preventDefault();
            self.showModal();
        };
        self.button_modal.addEventListener('click', onmodal);
        self.button_modal.addEventListener('keypress', onmodal);

        var onclose = function(ev) {
            if(self.touch_data.noclick) {
                self.touch_data.noclick = false;
                ev.preventDefault();
                return;
            }
            var key = ev.key;
            if(ev.type==='keypress' && key!==" " && key!=="Enter") {
                return;
            }
            ev.preventDefault();
            self.closeModal();
        };

        self.node_mask.addEventListener('click', onclose);
        self.node_dialog.addEventListener('click', function(ev) {ev.stopPropagation();});
        self.dialog_button_close_icon.addEventListener('click', onclose);
        self.dialog_button_close_icon.addEventListener('keypress', onclose);

        if(!self.oneimage) {
            if(self.options.timer){
                setInterval(function(){
                    self.next();
                }, self.options.timer*1000);
            }

            var startSwipe = function(ev) {self.startSwipe(ev);};
            var moveSwipe = function(ev) {self.moveSwipe(ev);};
            var endSwipe = function(ev) {self.endSwipe(ev);};

            self.node_mask.addEventListener('touchstart', startSwipe);
            self.node_mask.addEventListener('touchmove', moveSwipe);
            self.node_mask.addEventListener('touchend', endSwipe);
            self.node_mask.addEventListener('touchcancel', endSwipe);

            self.node_target.addEventListener('touchstart', startSwipe);
            self.node_target.addEventListener('touchmove', moveSwipe);
            self.node_target.addEventListener('touchend', endSwipe);
            self.node_target.addEventListener('touchcancel', endSwipe);

            self.node_mask.addEventListener('mousedown', startSwipe);
            self.node_mask.addEventListener('mousemove', moveSwipe);
            self.node_mask.addEventListener('mouseup', endSwipe);

            self.node_target.addEventListener('mousedown', startSwipe);
            self.node_target.addEventListener('mousemove', moveSwipe);
            self.node_target.addEventListener('mouseup', endSwipe);

            startSwipe = function(ev) {
                if(ev.type !== 'touchstart') {
                    ev.preventDefault();
                }
                self.startSwipe(ev);
            };
            moveSwipe = function(ev) {
                if(ev.type !== 'touchmove') {
                    ev.preventDefault();
                }
                self.moveSwipe(ev);
            };
            endSwipe = function(ev) {
                if(ev.type !== 'touchend' && ev.type !== 'touchcancel') {
                    ev.preventDefault();
                }
                self.endSwipe(ev);
            };

            self.node_image.addEventListener('touchstart', startSwipe);
            self.node_image.addEventListener('touchmove', moveSwipe);
            self.node_image.addEventListener('touchend', endSwipe);
            self.node_image.addEventListener('touchcancel', endSwipe);

            self.dialog_image.addEventListener('touchstart', startSwipe);
            self.dialog_image.addEventListener('touchmove', moveSwipe);
            self.dialog_image.addEventListener('touchend', endSwipe);
            self.dialog_image.addEventListener('touchcancel', endSwipe);

            self.node_image.addEventListener('mousedown', startSwipe);
            self.node_image.addEventListener('mousemove', moveSwipe);
            self.node_image.addEventListener('mouseup', endSwipe);

            self.dialog_image.addEventListener('mousedown', startSwipe);
            self.dialog_image.addEventListener('mousemove', moveSwipe);
            self.dialog_image.addEventListener('mouseup', endSwipe);

            var onprev = function(ev) {
                var key = ev.key;
                if(ev.type==='keypress' && key!==" " && key!=="Enter") {
                    return;
                }
                ev.preventDefault();
                self.prev();
            };

            var onnext = function(ev) {
                var key = ev.key;
                if(ev.type==='keypress' && key!==" " && key!=="Enter") {
                    return;
                }
                ev.preventDefault();
                self.next();
            };

            self.button_prev.addEventListener('keypress', onprev);
            self.button_prev.addEventListener('click', onprev);

            self.button_next.addEventListener('keypress', onnext);
            self.button_next.addEventListener('click', onnext);

            self.dialog_button_prev.addEventListener('keypress', onprev);
            self.dialog_button_prev.addEventListener('click', onprev);

            self.dialog_button_next.addEventListener('keypress', onnext);
            self.dialog_button_next.addEventListener('click', onnext);

            self.dialog_image.addEventListener('click', function(ev) {
                if(self.touch_data.noclick) {
                    self.touch_data.noclick = false;
                    ev.preventDefault();
                    return;
                }
                var x = ev.layerX - ev.target.x;
                if(x < ev.target.width/2) {
                    self.prev();
                    ev.preventDefault();
                } else if(x > ev.target.width/2) {
                    self.next();
                    ev.preventDefault();
                }
            });

            self.node_slider.addEventListener('change', function() {
                var idx = self.node_slider.value - 1;
                self.node_thumbnails.querySelector('input[data-index="'+idx+'"]').click();
            });
        }

        self.data.forEach(function(image_data, idx) {
            var image_element = document.createElement('li');
            var image_button = document.createElement('input');
            image_button.setAttribute('type', 'radio');
            image_button.setAttribute('value', image_data.uri);
            image_button.setAttribute('name', self.target);
            image_button.setAttribute('data-index', idx);
            image_button.setAttribute('id', self.target+'-'+idx);
            if(idx===0) {
                image_button.checked = true;
            }

            image_element.appendChild(image_button);

            var image_label = document.createElement('label');
            image_label.setAttribute('for', self.target+'-'+idx);
            image_element.appendChild(image_label);

            var image_thumb = document.createElement('img');
            image_thumb.setAttribute('src', image_data.thumb);
            image_thumb.setAttribute('width', image_data.thumbsize[0]);
            image_thumb.setAttribute('heigh', image_data.thumbsize[1]);

            if(image_data.alt) {
                image_button.setAttribute('data-alt', image_data.alt);
                image_thumb.setAttribute('alt', image_data.alt);
            } else {
                image_thumb.setAttribute('alt', self.options.label_thumbnail);
            }

            if(image_data.title) {
                image_button.setAttribute('data-title', image_data.title);
            }
            if(image_data.hide_alt) {
                image_button.setAttribute('data-hide-alt', true);
            }
            if(image_data.hide_alt) {
                image_button.setAttribute('data-hide-title', true);
            }

            image_label.appendChild(image_thumb);
            self.node_thumbnails.appendChild(image_element);

            image_button.addEventListener('change', function() {self.changeImage();});
        });

        document.addEventListener('keydown', function(ev) {
            var key = ev.key;

            if(!self.node_dialog.open && !self.node_target.contains(document.activeElement)) {
                return;
            }

            if(!self.oneimage && key==="ArrowLeft") {
                self.prev();
                ev.preventDefault();
            } else if(!self.oneimage && key==="ArrowRight") {
                self.next();
                ev.preventDefault();
            } else if(key==="Escape") {
                self.closeModal();
                ev.preventDefault();
            }
        });

        if(self.node_dialog.showModal) {
            self.node_dialog.addEventListener('close', function() {
                self.closeModal();
            });
        }

        self.changeImage();
    }

    prev() {
        var self = this;
        if(!self.oneimage) {
            var idx = self.node_thumbnails.querySelector('input:checked').getAttribute('data-index');
            idx = parseInt(idx) - 1;
            if(idx < 0) {
                idx = self.data.length - 1;
            }
            document.getElementById(self.target+'-'+idx).checked = true;
            self.changeImage();
        }
    }

    next() {
        var self = this;
        if(!self.oneimage) {
            var idx = self.node_thumbnails.querySelector('input:checked').getAttribute('data-index');
            idx = parseInt(idx) + 1;
            if(idx > self.data.length - 1) {
                idx = 0;
            }
            document.getElementById(self.target+'-'+idx).checked = true;
            self.changeImage();
        }
    }

    changeImage() {
        var self = this;
        var current = self.node_thumbnails.querySelector('input:checked');
        var title = current.getAttribute('data-title');
        var alt = current.getAttribute('data-alt');
        var hide_title = current.hasAttribute('data-hide-title');
        var hide_alt = current.hasAttribute('data-hide-alt');
        var url = current.getAttribute('value');
        var hide_caption = true;
        var idx = parseInt(current.getAttribute('data-index'));

        if(!self.options.no_transition && !self.oneimage) {
            self.node_image.style.opacity = 0.2;
            self.dialog_image.style.opacity = 0.2;
        }

        if(!self.oneimage) {
            if(self.node_slider.value !== idx+1) {
                self.node_slider.value = idx + 1;
            }
            var current_img = current.nextSibling.childNodes[0];
            var offset = current_img.offsetLeft - self.node_thumbnails.offsetLeft;
            offset -= self.node_thumbnails.offsetWidth / 2;
            offset += current_img.offsetWidth / 2;
            self.node_thumbnails.scrollTo({
                left: offset,
                behavior: 'smooth',
            });
        }

        if(!hide_title && title) {
            self.node_caption.innerHTML = title;
            self.node_caption.hidden = false;
            self.dialog_title.innerHTML = title;
            self.dialog_title.hidden = false;
            self.dialog_title.removeAttribute('aria-hidden');
            hide_caption = false;
        } else if(title) {
            self.node_caption.innerHTML = '';
            self.node_caption.hidden = true;
            self.dialog_title.innerHTML = title;
            self.dialog_title.hidden = false;
            self.dialog_title.removeAttribute('aria-hidden');
        } else {
            self.node_caption.innerHTML = '';
            self.node_caption.hidden = true;
            self.dialog_title.innerHTML = '';
            self.dialog_title.hidden = true;
            self.dialog_title.setAttribute('aria-hidden', true);
        }

        if(!hide_alt && alt) {
            self.node_alt.innerHTML = alt;
            self.node_alt.hidden = false;
            hide_caption = false;
        } else {
            self.node_alt.innerHTML = '';
            self.node_alt.hidden = true;
        }

        if(hide_caption) {
            self.node_div_caption.hidden = true;
        } else {
            self.node_div_caption.hidden = false;
        }

        if(self.options.no_transition || self.oneimage) {
            self.node_image.setAttribute('src', url);
            self.dialog_image.setAttribute('src', url);
        } else {
            setTimeout(function() {
                self.node_image.setAttribute('src', url);
                self.dialog_image.setAttribute('src', url);
                setTimeout(function() {
                    self.node_image.style.opacity = 1;
                    self.dialog_image.style.opacity = 1;
                }, 200);
            }, 200);
        }
    }

    showModal() {
        this.node_mask.hidden = false;
        this.node_mask.removeAttribute('aria-hidden');
        if(this.node_dialog.showModal) {
            this.node_dialog.showModal();
        } else {
            this.node_dialog.open = true;
            this.node_dialog.setAttribute('open', true);
            this.node_dialog.setAttribute('aria-modal', true);
            this.node_dialog.hidden = false;
            this.node_dialog.removeAttribute('aria-hidden');
        }
    }

    closeModal() {
        if(this.node_dialog.showModal) {
            this.node_dialog.close();
        } else {
            this.node_dialog.open = false;
            this.node_dialog.removeAttribute('open');
            this.node_dialog.removeAttribute('aria-modal');
            this.node_dialog.hidden = true;
            this.node_dialog.setAttribute('aria-hidden', true);
        }
        this.node_mask.hidden = true;
        this.node_mask.setAttribute('aria-hidden', true);
    }

    startSwipe(ev) {
        var self = this;
        if(!self.oneimage && self.touch_data.id === -1) {
            if(ev.type === 'touchstart') {
                self.touch_data.id = ev.changedTouches[0].identifier;
                self.touch_data.x = ev.changedTouches[0].clientX;
                self.touch_data.y = ev.changedTouches[0].clientY;
            } else {
                self.touch_data.id = -2;
                self.touch_data.x = ev.clientX;
                self.touch_data.y = ev.clientY;
            }
            self.touch_data.current_x = self.touch_data.x;
            self.touch_data.current_y = self.touch_data.y;

            if(!self.touch_data.interval) {
                self.touch_data.interval = setInterval(function() {
                    self.swipeItem();
                }, self.swipe_delay);
            }
        }
    }

    moveSwipe(ev) {
        var self = this;
        var move = false;
        var touch = null;

        if(!self.oneimage && self.touch_data.x) {
            if(ev.type === 'touchmove') {
                for(var i=0; i<ev.changedTouches.length; i++) {
                    touch = ev.changedTouches[i];
                    if(touch.identifier === self.touch_data.id) {
                        move = true;
                        self.touch_data.current_x = touch.clientX;
                    }
                }
            } else if(ev.which > 0) {
                move = true;
                self.touch_data.current_x = ev.clientX;
            }
        }
    }

    endSwipe(ev) {
        var self = this;
        var stop = false;
        var touch = null;

        if(!self.oneimage && self.touch_data.x) {
            if(ev.type === "touchend" || ev.type === "touchcancel") {
                for(var i=0; i<ev.changedTouches.length; i++) {
                    touch = ev.changedTouches[i];
                    if(touch.identifier === self.touch_data.id) {
                        stop = true;
                        self.touch_data.current_x = touch.clientX;
                        self.touch_data.current_y = touch.clientY;
                    }
                }
            } else {
                stop = true;
                self.touch_data.current_x = ev.clientX;
                self.touch_data.current_y = ev.clientY;
            }

            if(stop) {
                self.touch_data.id = -1;
                if(self.touch_data.interval) {
                    clearInterval(self.touch_data.interval);
                    self.touch_data.interval = null;
                }
                if(!self.touch_data.swiped) {
                    self.swipeItem();
                }

                if(self.touch_data.swiped) {
                    self.touch_data.noclick = true;
                    setTimeout(function() {
                        self.touch_data.noclick = false;
                    }, 300);
                }

                self.touch_data.x = null;
                self.touch_data.y = null;
                self.touch_data.current_x = null;
                self.touch_data.current_y = null;
                self.touch_data.swiped = false;
            }
        }
    }

    swipeItem() {
        var self = this;
        var width = self.touch_data.current_x - self.touch_data.x;
        var height = self.touch_data.current_y - self.touch_data.y;

        if(Math.abs(width) > self.getMinWidthSwipe()) {
            if(width < 0) {
                self.next(true);
                self.touch_data.swiped = true;
            } else {
                self.prev(true);
                self.touch_data.swiped = true;
            }
        } else if(Math.abs(height) > self.node_mask.clientHeight/3) {
            self.closeModal();
            self.touch_data.swiped = true;
        }
    }

    getMinWidthSwipe() {
        if(this.node_mask.hidden) {
            return this.node_image.clientWidth/3;
        }
        return this.dialog_image.clientWidth/3;
    }
}
