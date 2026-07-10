from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import (
    Category, SubCategory, Product, ProductImage, HeroSection, EditorialSection,
    WhyChooseUsCard, HeritageSection, ProcessStep, TechnicalMetric,
    ExportCountry, Testimonial, FaqItem
)

class Command(BaseCommand):
    help = "Seed the database with categories, subcategories, products, and default homepage configs."

    def handle(self, *args, **options):
        self.stdout.write("Deleting existing seed data...")
        Category.objects.all().delete()
        HeroSection.objects.all().delete()
        EditorialSection.objects.all().delete()
        WhyChooseUsCard.objects.all().delete()
        HeritageSection.objects.all().delete()
        ProcessStep.objects.all().delete()
        TechnicalMetric.objects.all().delete()
        ExportCountry.objects.all().delete()
        Testimonial.objects.all().delete()
        FaqItem.objects.all().delete()

        self.stdout.write("Creating categories and subcategories...")
        
        # 1. SAREES
        sarees = Category.objects.create(
            name="Sarees", 
            description="Bengal's finest handloom and heritage silk/cotton sarees."
        )
        saree_subs = [
            "Pure Tussar Silk", "Premium Mul Cotton", "Bagru Handblock Prints & Paints", 
            "Hand Painted Boutique Sarees (4 Ply Bishnupuri Silk)", "Jamdani", 
            "Pure 100 Count Linen", "Handwoven 120 Count Khadi", "Handwoven Khadi Silk", 
            "Fancy Art Silk", "Cotton Silk", "Hand Painted Premium Sarees", "Banarasi Silk", 
            "Satin Silk", "Viscose Sarees", "Pure Matka Silk", "Semi Matka", "Semi Tussar", 
            "Handcrafted Sarees", "Premium Tissue Khadi", "Premium Tissue Silk", 
            "Premium Tissue Kanchi Silk", "Surat Silk"
        ]
        saree_sub_objs = {}
        for sname in saree_subs:
            s_obj = SubCategory.objects.create(category=sarees, name=sname)
            saree_sub_objs[sname] = s_obj

        # 2. KURTIS
        kurtis = Category.objects.create(
            name="Kurtis",
            description="Haute couture handcrafted and painted kurtis for boutique retail."
        )
        kurti_subs = [
            "Handcrafted Silk Kurtis", "Pure Modal Silk Kurtis", "Pure Cotton Kurtis",
            "Hand Painted Kurtis", "Kantha Stitch Kurtis", "Pure Malai Cotton Kurtis"
        ]
        kurti_sub_objs = {}
        for sname in kurti_subs:
            s_obj = SubCategory.objects.create(category=kurtis, name=sname)
            kurti_sub_objs[sname] = s_obj

        # 3. SUIT PIECES
        suits = Category.objects.create(
            name="Suit Pieces",
            description="Premium unstitched salwar suit materials."
        )
        suit_subs = [
            "Cotton Suit Pieces", "Silk Suit Pieces", "Semi Silk Suit Pieces", "Viscose Suit Pieces"
        ]
        suit_sub_objs = {}
        for sname in suit_subs:
            s_obj = SubCategory.objects.create(category=suits, name=sname)
            suit_sub_objs[sname] = s_obj

        # 4. BLOUSES
        blouses = Category.objects.create(
            name="Blouses",
            description="Exquisite designer blouses, hand-painted and embroidery-rich."
        )
        blouse_subs = [
            "Handcrafted Blouses", "Hand Painted Blouses", "Kantha Stitch Blouses",
            "Embroidery Designer Blouses", "Pure Cotton Blouses", "Handblock Printed Blouses"
        ]
        blouse_sub_objs = {}
        for sname in blouse_subs:
            s_obj = SubCategory.objects.create(category=blouses, name=sname)
            blouse_sub_objs[sname] = s_obj

        # 5. NIGHTIES
        nighties = Category.objects.create(
            name="Nighties",
            description="Premium loungewear and comfortable printed cotton nighties."
        )
        nightie_subs = [
            "Cotton Nighties", "Printed Nighties", "Designer Nighties", "Premium Nighties", "Daily Wear Nighties"
        ]
        nightie_sub_objs = {}
        for sname in nightie_subs:
            s_obj = SubCategory.objects.create(category=nighties, name=sname)
            nightie_sub_objs[sname] = s_obj

        self.stdout.write("Seeding sample B2B products...")
        
        # Saree Products
        s1 = Product.objects.create(
            name="Garad Classic Standard",
            category=sarees,
            subcategory=saree_sub_objs["Handcrafted Sarees"],
            description="Traditional off-white mulberry silk saree with deep crimson border and raw silk texture.",
            purity_fabric="Grade AAAA Mulberry Raw Silk — Non-Bleached",
            border_specs="Solid Pure Crimson Weft Edge Banding",
            structural_weight="410 Grams Structural Array",
            moq="30 Units Minimum",
            material="Grade AAAA Mulberry",
            is_best_seller=True,
            is_silk_collection=True
        )
        ProductImage.objects.create(product=s1, image='products/gallery/garad_detail1.jpg', order=1)
        ProductImage.objects.create(product=s1, image='products/gallery/garad_detail2.jpg', order=2)
        
        s2 = Product.objects.create(
            name="Korial Imperial Luxury",
            category=sarees,
            subcategory=saree_sub_objs["Handcrafted Sarees"],
            description="Intense crimson border lined with 24K gold zari loops on a heavy off-white body.",
            purity_fabric="Premium Filament Silk Weft Mesh",
            border_specs="Concentric Fine Zari Geometric Run Bands — 24K Gold",
            structural_weight="490 Grams Heavy Premium Grade",
            moq="20 Units Minimum",
            material="24K Zari Border",
            is_new_arrival=True,
            is_silk_collection=True
        )
        ProductImage.objects.create(product=s2, image='products/gallery/korial_detail1.jpg', order=1)
        
        s3 = Product.objects.create(
            name="Tussar Korial Hybrid",
            category=sarees,
            subcategory=saree_sub_objs["Pure Tussar Silk"],
            description="Wild organic tussar silk body fused with traditional red korial zari borders.",
            purity_fabric="Wild Organic Tussar Core Filament Yarn",
            border_specs="Deep Ruby Red Selvedge Accent Bands",
            structural_weight="430 Grams Textural Open Mesh",
            moq="40 Units Minimum",
            material="Natural Tussar Silk",
            is_handcrafted=True
        )
        
        s4 = Product.objects.create(
            name="Baluchari Crimson Narrative",
            category=sarees,
            subcategory=saree_sub_objs["Handcrafted Sarees"],
            description="Exquisite mythological scenes woven into the endpiece (pallu) using high density raw silks.",
            purity_fabric="Dense Twist Pure Dyed Filament Base Silk",
            border_specs="Mythological Silhouette Pallu Panels — Jacquard",
            structural_weight="560 Grams Narrative Art Weave",
            moq="12 Units Minimum",
            material="Artisanal Heritage",
            is_best_seller=True,
            is_festive_collection=True
        )

        s5 = Product.objects.create(
            name="Matka Silk Gold Shimmer",
            category=sarees,
            subcategory=saree_sub_objs["Pure Matka Silk"],
            description="Premium rough texture matka silk with fine gold zari weaves on borders.",
            purity_fabric="Pure Hand-spun Matka Silk Yarn",
            border_specs="Zari Accent Borders",
            structural_weight="450 Grams",
            moq="15 Units Minimum",
            material="Matka Silk",
            is_premium=True
        )

        # Kurti Products
        k1 = Product.objects.create(
            name="Modal Silk Royal Kurti",
            category=kurtis,
            subcategory=kurti_sub_objs["Pure Modal Silk Kurtis"],
            description="Premium modal silk kurti with hand-block print overlays and side slits.",
            purity_fabric="100% Pure Modal Silk",
            border_specs="Intricate Handblock Prints",
            structural_weight="250 Grams",
            moq="50 Units Minimum",
            material="Modal Silk",
            is_best_seller=True,
            is_silk_collection=True
        )
        ProductImage.objects.create(product=k1, image='products/gallery/modal_kurti_detail.jpg', order=1)

        k2 = Product.objects.create(
            name="Kantha Stitch Premium Kurti",
            category=kurtis,
            subcategory=kurti_sub_objs["Kantha Stitch Kurtis"],
            description="Fine hand embroidery on high thread count cotton base.",
            purity_fabric="Premium Khadi Cotton",
            border_specs="Hand Kantha Stitch Panel Work",
            structural_weight="220 Grams",
            moq="25 Units Minimum",
            material="Handwoven Cotton",
            is_handcrafted=True,
            is_cotton_collection=True
        )

        # Blouse Products
        b1 = Product.objects.create(
            name="Hand Painted Madhubani Blouse",
            category=blouses,
            subcategory=blouse_sub_objs["Hand Painted Blouses"],
            description="Premium Bishnupuri silk blouse hand-painted by traditional artists.",
            purity_fabric="4 Ply Bishnupuri Silk",
            border_specs="Madhubani Handpainted Scenic Back",
            structural_weight="150 Grams",
            moq="10 Units Minimum",
            material="Bishnupuri Silk",
            is_hand_painted=True,
            is_best_seller=True
        )

        # Nighties Products
        n1 = Product.objects.create(
            name="Premium Floral Cotton Nighty",
            category=nighties,
            subcategory=nightie_sub_objs["Premium Nighties"],
            description="Comfortable daily wear nighty woven in high count cotton.",
            purity_fabric="100% Cotton 60s Count",
            border_specs="Printed Selvedge Details",
            structural_weight="180 Grams",
            moq="100 Units Minimum",
            material="Pure Cotton",
            is_cotton_collection=True,
            is_sale=True
        )

        self.stdout.write("Seeding sections configurations...")
        
        # Hero Section
        HeroSection.objects.create(
            eyebrow="Direct Manufacturer · Export House · OEM · Private Label",
            title="Bengal's Finest",
            highlighted_title="Handloom Sarees",
            description="Premium B2B Manufacturer & Global Export Partner for Luxury Boutiques, Fashion Houses & International Retail Chains. Garad · Korial · Baluchari · Jamdani.",
            primary_cta_text="Explore Collection",
            secondary_cta_text="Become Wholesale Partner",
            stats_years="52+",
            stats_retailers="500+",
            stats_countries="42",
            stats_variants="12K+"
        )

        # Editorials
        EditorialSection.objects.create(
            section_id="editorial_1",
            tag="Silk Engineering",
            title="Pure <strong>Garad</strong> &amp;",
            highlighted_title="Korial Heritage",
            description="The off-white mulberry core of the Garad saree carries centuries of Bengali ritual heritage. Each warp thread is sourced from select mulberry clusters and woven by master artisans trained through generations of guild knowledge.",
            bullet_points=(
                "Grade AAAA Non-Bleached Mulberry Raw Silk\n"
                "Traditional Hand-wound Zari Paar Borders\n"
                "Bishnupur & Murshidabad GI-Tagged Origin\n"
                "Structural Weight: 380–600 grams per piece\n"
                "Color Fastness: ISO 105-C06 Grade 4–5"
            ),
            button_text="View Full Collection",
            is_reversed=False
        )

        EditorialSection.objects.create(
            section_id="editorial_2",
            tag="Direct Procurement",
            title="Loom to <strong>Boutique</strong>",
            highlighted_title="Zero Margin Loss",
            description="Every transaction routes natively through our cluster procurement centers. We eliminate all intermediary margins. International boutiques access verified handloom inventory at true wholesale rates.",
            bullet_points=(
                "Direct cluster sourcing — zero middlemen\n"
                "Quarterly social & infrastructure audits\n"
                "International shipping to 42 countries\n"
                "Dedicated B2B account manager on each order\n"
                "OEM & Private Label programs available"
            ),
            button_text="Access Master Catalog",
            is_reversed=True
        )

        # Why Choose Us
        why_cards = [
            ("Direct Manufacturer", "🏭", "We own the looms. No agents, no brokers. Direct factory pricing ensures your margins remain strong.", 0),
            ("Private Label & OEM", "🏷️", "Complete private label manufacturing. Your brand, your labels, your packaging. Custom weave specifications supported.", 1),
            ("Worldwide Shipping", "🌍", "Established export infrastructure to 42 countries. Full documentation — GSP, COO, quality certificates.", 2),
            ("Premium Quality Control", "✦", "ISO 9001:2015 certified processes. Every piece undergoes 14-point inspection before packaging.", 3),
        ]
        for title, icon, desc, order in why_cards:
            WhyChooseUsCard.objects.create(title=title, icon=icon, description=desc, order=order)

        # Heritage Section
        HeritageSection.objects.create(
            label="Our Heritage",
            title="Five Centuries of",
            highlighted_title="Bengali Silk Mastery",
            body_p1="Rooted in the handloom heartlands of Bishnupur, Murshidabad, and Shantipur, Jyoticreations was founded to bridge Bengal's finest handloom artisans with global luxury commerce. Our sarees carry an unbroken thread of craftsmanship stretching back five hundred years.",
            body_p2="We operate exclusively as a B2B platform — no retail, no compromise. Enterprise clients from Paris, London, New York, Dubai and Singapore trust our verification protocols and cluster compliance frameworks built over decades.",
            specs_iso="9001:2015",
            specs_gi="Registered",
            specs_established="Est. 2008",
            specs_license="Active · 42 Nations",
            button_text="Begin B2B Partnership"
        )

        # Process Steps
        steps = [
            ("01", "🌿", "Silk Selection", 0),
            ("02", "🎨", "Natural Dyeing", 1),
            ("03", "🧵", "Warping", 2),
            ("04", "⚙️", "Handloom Weaving", 3),
            ("05", "✨", "Zari Embroidery", 4),
            ("06", "🔍", "QC Inspection", 5),
            ("07", "📦", "Luxury Packaging", 6),
        ]
        for num, icon, lbl, order in steps:
            ProcessStep.objects.create(step_number=num, icon=icon, label=lbl, order=order)

        # Tech Metrics
        metrics = [
            ("Tensile Warp Resilience", "9.4 N/Tex — Military-Grade Warp Integrity", "Certified", 0),
            ("Color Fastness Rating", "ISO 105-C06 — Grade 4–5 Wet & Dry", "Tested", 1),
            ("Zari Thread Purity", "24K Micron Gold-Plated Metallic Core", "Verified", 2),
            ("Shrinkage Resistance", "< 2% Post-Wash — Certified Dimensional Stability", "Certified", 3),
            ("Weave Density", "140–220 Picks Per Inch — Artisanal Grade", "Premium", 4),
        ]
        for lbl, val, tag, order in metrics:
            TechnicalMetric.objects.create(label=lbl, value=val, status_tag=tag, order=order)

        # Export Countries
        countries = [
            ("🇺🇸", "United States", "Premium Market", 0),
            ("🇬🇧", "United Kingdom", "Luxury Retail", 1),
            ("🇦🇪", "United Arab Emirates", "Flagship Market", 2),
            ("🇫🇷", "France", "Fashion Capital", 3),
            ("🇸🇬", "Singapore", "Asia Pacific Hub", 4),
        ]
        for flag, name, tag, order in countries:
            ExportCountry.objects.create(flag=flag, name=name, tag=tag, order=order)

        # Testimonials
        testimonials = [
            ("The Korial Zari collection outsold every other saree line in our Dubai flagship within two weeks. The quality verification and GI documentation give us complete confidence.", "Arjun Mehta", "Head of Procurement, Al Noor Textiles", "UAE · Dubai", 0),
            ("We've sourced Indian textiles for 15 years. Jyoticreations is the only vendor who provides loom-origin documentation with every shipment.", "Sophia Laurent", "Creative Director, Maison de Soie", "France · Paris", 1),
        ]
        for quote, author, role, loc, order in testimonials:
            Testimonial.objects.create(quote=quote, author=author, role=role, location=loc, order=order)

        # FAQs
        faqs = [
            ("What is the Minimum Order Quantity (MOQ)?", "Our standard B2B MOQ starts at 10 units for active inventory collections and 25-50 units for custom OEM/private label designs.", 0),
            ("Do you provide GI origin certificates?", "Yes, all our Baluchari, Garad, and Jamdani sarees are supplied with authentic Geographical Indication (GI) tag certification cards.", 1),
            ("How long is the B2B production cycle?", "Standard catalog allocations ship within 14-21 days. Custom weave or private label orders typically require 28-45 days depending on complexity.", 2),
        ]
        for q, a, order in faqs:
            FaqItem.objects.create(question=q, answer=a, order=order)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with premium B2B categories and products!"))
