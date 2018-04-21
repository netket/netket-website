---
title: Tutorials
permalink: /tutorials/home/
redirect_from: /tutorials/index.html
---


<br>

{% assign kfile = 1 %}
{% for file in site.data.tutorials %}

{% assign item_url = file | prepend:"/tutorials/" | append:"/" %}
{% assign p = site.tutorials | where:"url", item_url | first %}

{% assign rem = kfile | modulo: 2 %}

{% if rem == 1 %}
<div class="row ">
{% endif %}

<div class="col-sm-6">
<div class="panel panel-default">
  <div class="panel-heading">
    <h4>
    <a href="{{ p.url  | prepend: site.baseurl }}"> {{ p.title }} </a>
    </h4>
  </div>
  <div class="panel-body">
  <p>{{ p.description }}</p>
  </div>
</div>
</div>

{% if rem == 0 or kfile == site.data.tutorials.size %}
</div>
{% endif %}

{% assign kfile = kfile | plus: 1 %}
{% endfor %}
