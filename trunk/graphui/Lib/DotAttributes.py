# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

dot_args = '''
      Name      UsedBy     Type         
 Damping         G       double      0.99              0.0       neato only
 Epsilon         G       double      (.0001 * # nodes)           neato only
 URL             ENGC    string
 arrowhead       E       arrowType   normal
 arrowsize       E       double      1.0               0.0
 arrowtail       E       arrowType   normal
 bb              G       rect                                    write-only
 bgcolor         G       color
 bottomlabel     N       string      ""
 center          G       bool        false
 clusterrank     G       clusterMode local                       dot only
 color           ENC     color       black
 comment         ENG     string      ""
 compound        G       bool        false                       dot only
 concentrate     G       bool        false                       dot only
 constraint      E       bool        true                        dot only
 decorate        E       bool        false
 dir             E       dirType     forward(directed)
 distortion      N       double      0.0               -100.0
 fillcolor       NC      color       lightgrey(nodes)
 fixedsize       N       bool        false
 fontcolor       ENGC    color       black
 fontname        ENGC    string      "Times-Roman"
 fontpath        G       string      ""
 fontsize        ENGC    double      14.0              1.0
 group           N       string      ""                          dot only
 headURL         E       string      ""
 headlabel       E       string      ""
 headport        E       portPos     center
 height          N       double      0.5               0.02
 label           ENGC    string      ""
 labelangle      E       double      -25.0             -180.0
 labeldistance   E       double      1.0               0.0
 labelfloat      E       bool        false
 labelfontcolor  E       color       black
 labelfontname   E       string      "Times-Roman"
 labelfontsize   E       double      11.0              1.0
 labeljust       C       string      ""                          dot only
 labelloc        GC      string      "t"(clusters)               dot only
 layer           EN      layerRange  ""
 layers          G       layerList   ""
 len             E       double      1.0                         neato only
 lhead           E       string      ""                          dot only
 lp              EGC     point                                   write-only
 ltail           E       string      ""                          dot only
 margin          G       double
 maxiter         G       int         MAXINT                      neato only
 mclimit         G       double      1.0                         dot only
 minlen          E       int         1                 0         dot only
 model           G       string      ""                          neato only
 nodesep         G       double      0.25              0.02      dot only
 normalize       G       bool        false                       neato only
 nslimit
 nslimit1        G       double                                  dot only
 ordering        G       string      ""                          dot only
 orientation     N       double      0.0               360.0
 orientation     G       string      ""
 overlap         G       string      ""                          neato only
 page            G       pointf
 pagedir         G       pagedir     BL
 peripheries     N       int                           0
 pin             N       bool                                    neato only
 pos             EN      point
 quantum         G       double      0.0               0.0
 rank            S       rankType                                dot only
 rankdir         G       rankdir     TB                          dot only
 ranksep         G       double      0.5               0.02
 ratio           G       double
 rects           N       rect                                    write-only
 regular         N       bool        false
 remincross      G       bool        false                       dot only
 rotate          G       int         0
 samehead        E       string      ""                          dot only
 sametail        E       string      ""                          dot only
 samplepoints    G       int         8
 searchsize      G       int         30                          dot only
 sep             G       double      0.01                        neato only
 shape           N       shape       ellipse
 shapefile       N       string      ""
 showboxes       ENG     int         0                 0         dot only
 sides           N       int         4                 0
 size            G       pointf
 skew            N       double      0.0               -100.0
 splines         G       bool        false                       neato only
 start           G       string      ""                          neato only
 style           ENC     style
 styleheet       G       style
 tailURL         E       string      ""
 taillabel       E       string      ""
 tailport        E       portPos     center
 toplabel        N       string      ""
 vertices        N       pointfList                              write-only
 voro_margin     G       double      0.05              0.0       neato only
 w               E       double      1.0                         neato only
 weight          E       double      1.0               0(dot)
 width           N       double      0.75              0.01
 z               N       double      0.0               -MAXFLOAT
'''

lines = dot_args.split('\n')
header = lines[1].split()
arg_list = []
for line in lines[2:]:
    if 'neato only' in line:
        continue
    # We don't care about the default, minimum, or Notes
    arg_list.append(line.lower().split()[:len(header)])
    
