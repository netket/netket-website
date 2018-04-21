---
title: Documentation
permalink: /docs/home/
redirect_from: /docs/index.html
layout: tutorials
---
<br>

{% assign kfile = 1 %}
{% for section in site.data.docs %}

{% assign rem = kfile | modulo: 3 %}

{% if rem == 1 %}
<div class="row ">
{% endif %}

<div class="col-sm-4">
<div class="panel panel-default">
  <div class="panel-heading">
    <h4>
    {{section.title}}
    </h4>
  </div>
  <ul class="list-group">
  {% for item in section.docs %}
    {% assign item_url = item | prepend:"/docs/" | append:"/" %}
    {% assign p = site.docs | where:"url", item_url | first %}
    <a class="list-group-item" href="{{ p.url  | prepend: site.baseurl }}">{{ p.title }}</a>
  {% endfor %}
  </ul>
</div>
</div>

{% if rem == 0  %}
</div>
{% endif %}

{% assign kfile = kfile | plus: 1 %}
{% endfor %}
