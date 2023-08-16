<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text"/>
    <xsl:template match="*">
        <xsl:choose>
            <xsl:when test="string-length(name()) = 3">
                <!-- Section Node -->
                <xsl:text>!</xsl:text>
                <xsl:value-of select="name()"/>
                <xsl:text>:</xsl:text>
                <xsl:text>&#10;</xsl:text>
                <xsl:apply-templates select="*"/>
                <xsl:text>!END</xsl:text>
                <xsl:value-of select="name()"/>
                <xsl:text>&#10;</xsl:text>                
            </xsl:when>
            <xsl:otherwise>
                <!-- Value Node -->
                <xsl:text>$</xsl:text>
                <xsl:value-of select="name()"/>
                <xsl:text>=</xsl:text>
                <xsl:value-of select="text()"/>
                <xsl:text>|</xsl:text>
                <xsl:text>&#10;</xsl:text>
            </xsl:otherwise>
        </xsl:choose> 
    </xsl:template>
</xsl:stylesheet>
