package
{
   import spark.components.Application;
   import spark.components.BorderContainer;
   import mx.controls.Image;
   import mx.core.IFlexModuleFactory;
   import flash.events.Event;
   import flash.display.Loader;
   import mx.utils.URLUtil;
   import flash.net.URLRequest;
   import flash.display.Bitmap;
   import flash.display.BitmapData;
   import flash.events.MouseEvent;
   import flash.net.navigateToURL;
   import mx.binding.BindingManager;
   import mx.core.DeferredInstanceFromFunction;
   import spark.components.Label;
   import mx.core.mx_internal;
   import mx.styles.CSSStyleDeclaration;
   import mx.styles.CSSCondition;
   import mx.styles.CSSSelector;
   import mx.events.PropertyChangeEvent;
   
   public class ShowThePage extends Application
   {
       
      private var _342656334pageContainer:BorderContainer;
      
      private var _1350568288thePage:Image;
      
      private var __moduleFactoryInitialized:Boolean = false;
      
      private var topLeft_x:Number;
      
      private var topLeft_y:Number;
      
      private var bottomRight_x:Number;
      
      private var bottomRight_y:Number;
      
      private var originalWidth:Number;
      
      private var originalHeight:Number;
      
      private var bookID:String;
      
      private var pageID:String;
      
      private var version:String;
      
      mx_internal var _ShowThePage_StylesInit_done:Boolean = false;
      
      public function ShowThePage()
      {
         super();
         this.width = 820;
         this.minWidth = 955;
         this.minHeight = 600;
         this.mxmlContentFactory = new DeferredInstanceFromFunction(this._ShowThePage_Array1_c);
         this.addEventListener("addedToStage",this.___ShowThePage_Application1_addedToStage);
      }
      
      override public function set moduleFactory(param1:IFlexModuleFactory) : void
      {
         super.moduleFactory = param1;
         if(this.__moduleFactoryInitialized)
         {
            return;
         }
         this.__moduleFactoryInitialized = true;
         mx_internal::_ShowThePage_StylesInit();
      }
      
      override public function initialize() : void
      {
         super.initialize();
      }
      
      protected function application1_addedToStageHandler(param1:Event) : void
      {
         this.bookID = this.loaderInfo.parameters["bookID"];
         this.pageID = this.loaderInfo.parameters["pageID"];
         var _loc2_:String = this.loaderInfo.parameters["characterFile"];
         var _loc3_:String = this.loaderInfo.parameters["pageSize"];
         this.version = this.loaderInfo.parameters["version"];
         this.getCoordinationBeforeChange(_loc2_);
         this.getOriginalSize(_loc3_);
      }
      
      private function getCoordinationBeforeChange(param1:String) : void
      {
         if(param1 == null || param1.length == 0)
         {
            return;
         }
         var _loc2_:String = param1.substring(param1.indexOf("(") + 1,param1.indexOf(")"));
         var _loc3_:Array = _loc2_.split(",");
         // These represent the coordinates of the drawn box
         this.topLeft_x = Number(_loc3_[0]);
         this.topLeft_y = Number(_loc3_[1]);
         this.bottomRight_x = Number(_loc3_[2]);
         this.bottomRight_y = Number(_loc3_[3]);
      }
      
      private function getOriginalSize(param1:String) : void
      {
         if(param1 == null || param1.length == 0)
         {
            return;
         }
         var _loc2_:Array = param1.split("-");
         this.originalWidth = Number(_loc2_[0]);
         this.originalHeight = Number(_loc2_[1]);
      }
      
      private function getNewPosition() : void
      {
         if(this.version == "new")
         {
            this.topLeft_x = this.topLeft_x * 5 / this.originalWidth * this.thePage.width;
            this.topLeft_y = this.topLeft_y * 5 / this.originalHeight * this.thePage.height;
            this.bottomRight_x = this.bottomRight_x * 5 / this.originalWidth * this.thePage.width;
            this.bottomRight_y = this.bottomRight_y * 5 / this.originalHeight * this.thePage.height;
         }
         else if(this.version == "old")
         {
            this.topLeft_x = this.topLeft_x * 6.27 / this.originalWidth * this.thePage.width - 3;
            this.topLeft_y = this.topLeft_y * 6.27 / this.originalHeight * this.thePage.height - 3;
            this.bottomRight_x = this.bottomRight_x * 6.27 / this.originalWidth * this.thePage.width + 3;
            this.bottomRight_y = this.bottomRight_y * 6.27 / this.originalHeight * this.thePage.height + 3;
         }
      }
      
      protected function thePage_addedToStageHandler(param1:Event) : void
      {
         var _loc3_:* = null;
         this.thePage.width = 800;
         this.thePage.height = this.thePage.width * this.originalHeight / this.originalWidth;
         this.getNewPosition();
         var _loc2_:Loader = new Loader();
         var _loc4_:String = this.url;
         var _loc5_:String = URLUtil.getServerName(_loc4_);
         if(_loc5_ != null && _loc5_.length == 21)
         {
            _loc3_ = "http://www.cadal.zju6.edu.cn/WebService/images/books/" + this.bookID + "/" + this.pageID + ".jpg";
         }
         else
         {
            _loc3_ = "http://www.cadal.zju.edu.cn/CalliSources/images/books/" + this.bookID + "/" + this.pageID + ".jpg";
         }
         var _loc6_:URLRequest = new URLRequest(_loc3_);
         _loc2_.load(_loc6_);
         _loc2_.contentLoaderInfo.addEventListener(Event.COMPLETE,this.onLoadComplete);
      }
      
      // Draws the red box by setting individual pixels red
      protected function onLoadComplete(param1:Event) : void
      {
          // I think loc4_ & loc5_ represent the outer-box, while loc
          
         var _loc4_:int = 0;
         var _loc5_:int = 0;
         var _loc2_:Bitmap = param1.target.content;
         var _loc3_:BitmapData = _loc2_.bitmapData;
         _loc4_ = this.topLeft_y - 3;
         while(_loc4_ < this.topLeft_y)
         {
            _loc5_ = this.topLeft_x - 3;
            while(_loc5_ < this.bottomRight_x + 3)
            {
               _loc3_.setPixel32(_loc5_,_loc4_,16711680);
               _loc5_++;
            }
            _loc4_++;
         }
         _loc4_ = this.bottomRight_y;
         while(_loc4_ < this.bottomRight_y + 3)
         {
            _loc5_ = this.topLeft_x - 3;
            while(_loc5_ < this.bottomRight_x + 3)
            {
               _loc3_.setPixel32(_loc5_,_loc4_,16711680);
               _loc5_++;
            }
            _loc4_++;
         }
         _loc4_ = this.topLeft_y - 3;
         while(_loc4_ < this.bottomRight_y + 3)
         {
            _loc5_ = this.topLeft_x - 3;
            while(_loc5_ < this.topLeft_x)
            {
               _loc3_.setPixel32(_loc5_,_loc4_,16711680);
               _loc5_++;
            }
            _loc4_++;
         }
         _loc4_ = this.topLeft_y - 3;
         while(_loc4_ < this.bottomRight_y + 3)
         {
            _loc5_ = this.bottomRight_x;
            while(_loc5_ < this.bottomRight_x + 3)
            {
               _loc3_.setPixel32(_loc5_,_loc4_,16711680);
               _loc5_++;
            }
            _loc4_++;
         }
         this.thePage.source = _loc3_;
         this.thePage.addChild(_loc2_);
      }
      
      protected function label1_clickHandler(param1:MouseEvent) : void
      {
         navigateToURL(new URLRequest("http://www.cadal.zju.edu.cn/book/tryBook/" + this.bookID + "/" + this.pageID));
      }
      
      private function _ShowThePage_Array1_c() : Array
      {
         var _loc1_:Array = [this._ShowThePage_BorderContainer1_i()];
         BindingManager.executeBindings(this,"temp",_loc1_);
         return _loc1_;
      }
      
      private function _ShowThePage_BorderContainer1_i() : BorderContainer
      {
         var _loc1_:BorderContainer = new BorderContainer();
         _loc1_.left = 0;
         _loc1_.right = 0;
         _loc1_.top = 0;
         _loc1_.bottom = 0;
         _loc1_.horizontalCenter = 0;
         _loc1_.verticalCenter = 0;
         _loc1_.mxmlContentFactory = new DeferredInstanceFromFunction(this._ShowThePage_Array2_c);
         _loc1_.id = "pageContainer";
         if(!_loc1_.document)
         {
            _loc1_.document = this;
         }
         this.pageContainer = _loc1_;
         BindingManager.executeBindings(this,"pageContainer",this.pageContainer);
         return _loc1_;
      }
      
      private function _ShowThePage_Array2_c() : Array
      {
         var _loc1_:Array = [this._ShowThePage_Label1_c(),this._ShowThePage_Image1_i(),this._ShowThePage_Label2_c(),this._ShowThePage_Label3_c()];
         BindingManager.executeBindings(this,"temp",_loc1_);
         return _loc1_;
      }
      
      private function _ShowThePage_Label1_c() : Label
      {
         var _loc1_:Label = new Label();
         _loc1_.x = 11;
         _loc1_.y = 10;
         _loc1_.height = 15;
         _loc1_.text = "红色框内为指定书法字位置，点击"; // Red box to specify the location of calligraphy , click
         if(!_loc1_.document)
         {
            _loc1_.document = this;
         }
         BindingManager.executeBindings(this,"temp",_loc1_);
         return _loc1_;
      }
      
      private function _ShowThePage_Image1_i() : Image
      {
         var _loc1_:Image = new Image();
         _loc1_.x = 10;
         _loc1_.y = 30;
         _loc1_.width = 800;
         _loc1_.addEventListener("addedToStage",this.__thePage_addedToStage);
         _loc1_.id = "thePage";
         if(!_loc1_.document)
         {
            _loc1_.document = this;
         }
         this.thePage = _loc1_;
         BindingManager.executeBindings(this,"thePage",this.thePage);
         return _loc1_;
      }
      
      public function __thePage_addedToStage(param1:Event) : void
      {
         this.thePage_addedToStageHandler(param1);
      }
      
      private function _ShowThePage_Label2_c() : Label
      {
         var _loc1_:Label = new Label();
         _loc1_.x = 195;
         _loc1_.y = 8;
         _loc1_.buttonMode = true;
         _loc1_.mouseChildren = false;
         _loc1_.text = "这里"; // Here
         _loc1_.useHandCursor = true;
         _loc1_.setStyle("color",354299);
         _loc1_.setStyle("fontSize",14);
         _loc1_.addEventListener("click",this.___ShowThePage_Label2_click);
         if(!_loc1_.document)
         {
            _loc1_.document = this;
         }
         BindingManager.executeBindings(this,"temp",_loc1_);
         return _loc1_;
      }
      
      public function ___ShowThePage_Label2_click(param1:MouseEvent) : void
      {
         this.label1_clickHandler(param1);
      }
      
      private function _ShowThePage_Label3_c() : Label
      {
         var _loc1_:Label = new Label();
         _loc1_.x = 231;
         _loc1_.y = 10;
         _loc1_.text = "跳转CADAL门户阅读"; // Jump CADAL portal Read
         if(!_loc1_.document)
         {
            _loc1_.document = this;
         }
         BindingManager.executeBindings(this,"temp",_loc1_);
         return _loc1_;
      }
      
      public function ___ShowThePage_Application1_addedToStage(param1:Event) : void
      {
         this.application1_addedToStageHandler(param1);
      }
      
      mx_internal function _ShowThePage_StylesInit() : void
      {
         var _loc1_:CSSStyleDeclaration = null;
         var _loc2_:Array = null;
         var _loc3_:Array = null;
         var _loc4_:CSSCondition = null;
         var _loc5_:CSSSelector = null;
         if(mx_internal::_ShowThePage_StylesInit_done)
         {
            return;
         }
         mx_internal::_ShowThePage_StylesInit_done = true;
         styleManager.initProtoChainRoots();
      }
      
      [Bindable(event="propertyChange")]
      public function get pageContainer() : BorderContainer
      {
         return this._342656334pageContainer;
      }
      
      public function set pageContainer(param1:BorderContainer) : void
      {
         var _loc2_:Object = this._342656334pageContainer;
         if(_loc2_ !== param1)
         {
            this._342656334pageContainer = param1;
            if(this.hasEventListener("propertyChange"))
            {
               this.dispatchEvent(PropertyChangeEvent.createUpdateEvent(this,"pageContainer",_loc2_,param1));
            }
         }
      }
      
      [Bindable(event="propertyChange")]
      public function get thePage() : Image
      {
         return this._1350568288thePage;
      }
      
      public function set thePage(param1:Image) : void
      {
         var _loc2_:Object = this._1350568288thePage;
         if(_loc2_ !== param1)
         {
            this._1350568288thePage = param1;
            if(this.hasEventListener("propertyChange"))
            {
               this.dispatchEvent(PropertyChangeEvent.createUpdateEvent(this,"thePage",_loc2_,param1));
            }
         }
      }
   }
}
