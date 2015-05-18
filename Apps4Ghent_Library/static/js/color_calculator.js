function ColorCalculator(lowestColor, highestColor, numberOfColors) {
  this.minColor = highestColor;
  this.maxColor = lowestColor;
  this.numberOfColors = numberOfColors;
}

ColorCalculator.prototype._calculateColorComponent = function(component, i) {
  var a = this.minColor[component];
  var b = this.maxColor[component];

  var index = this.numberOfColors - i - 1;

  return Math.floor(a + ((b - a) / this.numberOfColors) * index);
};

ColorCalculator.prototype._calculateColor = function(i) {
  return [0,1,2].map(function(component) {
    return this._calculateColorComponent(component, i);
  }.bind(this));
};

ColorCalculator.prototype.getValue = function(i) {
  var frac = (this.maxValue - this.minValue) / this.numberOfColors;
  return this.minValue + frac * i;
}

ColorCalculator.prototype.getColor = function(value) {
  for (var i=0; i < this.numberOfColors; ++i) {
    if (value < this.getValue(i)) return this._calculateColor(i);
  }

  return this._calculateColor(this.numberOfColors-1);
};

ColorCalculator.prototype.getRgbaColor = function(value, alpha) {
  var color = this.getColor(value);
  color.push(alpha);
  return 'rgba(' + color.join(', ') + ')';
};

ColorCalculator.prototype.update = function(values) {
  this.minValue = values[0];
  this.maxValue = values[0];

  values.forEach(function(val) {
    this.minValue = Math.min(val, this.minValue);
    this.maxValue = Math.max(val, this.maxValue);
  }.bind(this));
};
