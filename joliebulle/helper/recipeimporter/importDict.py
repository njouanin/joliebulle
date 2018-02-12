#!/usr/bin/python3
#­*­coding: utf­8 -­*­

#joliebulle 3.6
#Copyright (C) 2010-2014 Pierre Tavares
#Copyright (C) 2012-2013 joliebulle's authors
#See AUTHORS file.

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 3
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import logging
from model.constants import *
from model.fermentable import Fermentable
from model.hop import Hop
from model.mash import Mash
from model.mashstep import MashStep
from model.misc import Misc
from model.recipe import Recipe
from model.yeast import Yeast

logger = logging.getLogger(__name__)


def importDictRecipe(dic):
    logger.debug("Start parsing dict")

    recipe = Recipe()
    recipe.path = dic['path']
    recipe.name = dic['name']
    recipe.brewer = dic['brewer']
    recipe.style = dic['style']
    if dic['type'] == "All Grain":
        recipe.type = RECIPE_TYPE_ALL_GRAIN
    elif dic['type'] == "Extract":
        recipe.type = RECIPE_TYPE_EXTRACT
    elif recipe.type == "Partial Mash":
        recipe.type = RECIPE_TYPE_PARTIAL_MASH

    recipe.volume = dic['volume']
    recipe.boil = dic['boilTime']
    recipe.efficiency = dic['efficiency']

    for hop_dic in dic['hops']:
        hop = Hop()
        hop.name = hop_dic['name']

        if hop_dic['form'] == "Pellet":
            hop.form = HOP_FORM_PELLET
        elif hop_dic['form'] == "Leaf":
            hop.form = HOP_FORM_LEAF
        elif hop_dic['form'] == "Plug":
            hop.form = HOP_FORM_PLUG
        hop.alpha = hop_dic['alpha']
        hop.use = hop_dic['use']
        hop.time = hop_dic['time']
        hop.amount = hop_dic['amount']
        recipe.listeHops.append(hop)

    for f_dic in dic['fermentables']:
        f = Fermentable()
        f.name = f_dic['name']
        f.type = f_dic['type']
        f.fyield = f_dic['fyield']
        f.color = f_dic['color']
        f.amount = f_dic['amount']
        if f_dic['afterBoil'] == 'TRUE' :
            f.useAfterBoil = True
        else :
            f.useAfterBoil = False
        f.recommendMash = f_dic['recoMash']
        recipe.listeFermentables.append(f)

    for y_dic in dic['yeasts'] :
        y = Yeast()
        y.name = y_dic['name']
        y.productId = y_dic['product_id']
        y.labo = y_dic['labo']
        y.form = y_dic['form']
        y.attenuation = y_dic['attenuation']
        recipe.listeYeasts.append(y)

    for m_dic in dic['miscs'] :
        m = Misc()
        m.name = m_dic['name']
        m.amount = m_dic['amount']
        m.type = m_dic['type']
        m.use = m_dic['use']
        m.time = m_dic['time']
        recipe.listeMiscs.append(m)

    mash_dic = dic['mashProfile']
    recipe.mash.name = mash_dic['name']
    recipe.mash.ph = mash_dic['ph']
    recipe.mash.spargeTemp = mash_dic['sparge']
    recipe.mash.tunTemp = mash_dic['tunTemp']

    for s_dic in mash_dic['steps']:
        s = MashStep()
        s.name = s_dic['name']
        s.time = s_dic['time']
        s.temp = s_dic['temp']
        s.type = s_dic['type']
        recipe.listeMashSteps.append(s)
    recipe.recipeNotes = dic['notes']

    return recipe