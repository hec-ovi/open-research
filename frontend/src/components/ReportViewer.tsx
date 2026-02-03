/**
 * ReportViewer - Feature Component
 * 
 * Displays the final research report with markdown rendering
 * and download functionality (Markdown + PDF).
 */
import React from 'react';
import { motion } from 'framer-motion';
import { FileText, FileCode } from 'lucide-react';
import jsPDF from 'jspdf';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Button } from './ui/Button';
import { Card } from './ui/Card';
import { SourceViewer } from './SourceViewer';
import { useResearchStore } from '../stores/researchStore';
// Custom link component that opens in new tab
const MarkdownLink = ({ href, children }: { href?: string; children?: React.ReactNode }) => {
  return (
    <a 
      href={href} 
      target="_blank" 
      rel="noopener noreferrer"
      className="text-blue-400 hover:text-blue-300 hover:underline"
    >
      {children}
    </a>
  );
};

export function ReportViewer() {
  const { finalReport, status } = useResearchStore();

  if (!finalReport || status !== 'completed') return null;

  // Safety checks for report data - using snake_case from backend
  const title = finalReport.title || 'Untitled Report';
  const word_count = finalReport.word_count || 0;
  const sources_used = finalReport.sources_used || [];
  const sections = finalReport.sections || [];
  const executive_summary = finalReport.executive_summary || '';
  const confidence_assessment = finalReport.confidence_assessment || '';

  const handleDownloadMarkdown = () => {
    const markdown = `# ${finalReport.title}

${finalReport.executive_summary}

## Report Details

**Word Count:** ${finalReport.word_count}
**Sources Used:** ${sources_used.length}
**Confidence:** ${finalReport.confidence_assessment}

${finalReport.sections.map(s => `
## ${s.heading}

${s.content}
`).join('\n')}

## Sources

${sources_used.map((s, i) => `${i + 1}. [${s.title || 'Untitled'}](${s.url}) - ${s.reliability || 'unknown'}`).join('\n')}
`;

    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.toLowerCase().replace(/\s+/g, '-')}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadPDF = () => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 20;
    const maxWidth = pageWidth - margin * 2;
    let y = 20;

    // Helper function to add text with proper line height
    const addText = (text: string, x: number, yPos: number, options?: { maxWidth?: number; lineHeight?: number }) => {
      const opts = { maxWidth: maxWidth, lineHeight: 5, ...options };
      const lines = doc.splitTextToSize(text, opts.maxWidth!);
      doc.text(lines, x, yPos);
      return yPos + (lines.length * opts.lineHeight!);
    };

    // Helper to check page overflow
    const checkNewPage = (currentY: number, neededSpace: number = 30) => {
      if (currentY + neededSpace > pageHeight - margin) {
        doc.addPage();
        return margin + 10;
      }
      return currentY;
    };

    // ========== HEADER ==========
    // Title - centered, large, bold
    doc.setFontSize(24);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(33, 37, 41);
    const titleLines = doc.splitTextToSize(title, maxWidth);
    doc.text(titleLines, pageWidth / 2, y, { align: 'center' });
    y += (titleLines.length * 8) + 5;

    // Subtitle/Date
    doc.setFontSize(10);
    doc.setFont('helvetica', 'italic');
    doc.setTextColor(108, 117, 125);
    const date = new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    doc.text(`Research Report | ${date}`, pageWidth / 2, y, { align: 'center' });
    y += 12;

    // Horizontal line
    doc.setDrawColor(200, 200, 200);
    doc.line(margin, y, pageWidth - margin, y);
    y += 15;

    // ========== METADATA BOX ==========
    doc.setFillColor(248, 249, 250);
    doc.setDrawColor(222, 226, 230);
    doc.roundedRect(margin, y - 5, maxWidth, 20, 3, 3, 'FD');
    
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(73, 80, 87);
    const metaText = `Word Count: ${word_count} words | Sources: ${sources_used.length} | Confidence: ${confidence_assessment.split('.')[0] || 'High'}`;
    doc.text(metaText, pageWidth / 2, y + 7, { align: 'center' });
    y += 30;

    // ========== EXECUTIVE SUMMARY ==========
    y = checkNewPage(y, 60);
    
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(33, 37, 41);
    doc.text('Executive Summary', margin, y);
    y += 10;

    // Summary content with better formatting
    doc.setFontSize(11);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(52, 58, 64);
    
    // Clean up markdown for PDF
    const cleanSummary = executive_summary
      .replace(/\[🔗([^\]]+)\]\([^)]+\)/g, '$1') // Remove link markdown, keep text
      .replace(/\*\*/g, '') // Remove bold
      .replace(/\*/g, '') // Remove italic
      .replace(/#/g, '') // Remove headers
      .replace(/\n\n/g, '\n') // Normalize newlines
      .trim();
    
    y = addText(cleanSummary, margin, y, { lineHeight: 6 });
    y += 15;

    // ========== SECTIONS ==========
    sections.forEach((section, index) => {
      y = checkNewPage(y, 80);

      // Section heading with background
      doc.setFillColor(233, 236, 239);
      doc.roundedRect(margin, y - 6, maxWidth, 10, 2, 2, 'F');
      
      doc.setFontSize(13);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(33, 37, 41);
      doc.text(`${index + 1}. ${section.heading}`, margin + 3, y);
      y += 15;

      // Section content
      doc.setFontSize(10);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(52, 58, 64);
      
      // Clean content
      const cleanContent = section.content
        .replace(/\[🔗([^\]]+)\]\([^)]+\)/g, '$1 (source)')
        .replace(/\*\*/g, '')
        .replace(/\*/g, '')
        .replace(/#/g, '')
        .replace(/\n\n/g, '\n')
        .trim();
      
      y = addText(cleanContent, margin, y, { lineHeight: 5.5 });
      y += 12;
    });

    // ========== SOURCES PAGE ==========
    doc.addPage();
    y = margin + 10;

    // Sources header
    doc.setFontSize(18);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(33, 37, 41);
    doc.text('References & Sources', margin, y);
    y += 12;

    // Sources intro
    doc.setFontSize(10);
    doc.setFont('helvetica', 'italic');
    doc.setTextColor(108, 117, 125);
    doc.text(`This research is based on ${sources_used.length} authoritative sources.`, margin, y);
    y += 15;

    // Source list
    sources_used.forEach((source, index) => {
      y = checkNewPage(y, 40);

      // Source number box
      doc.setFillColor(33, 37, 41);
      doc.circle(margin + 3, y - 2, 4, 'F');
      doc.setFontSize(8);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(255, 255, 255);
      doc.text(String(index + 1), margin + 3, y - 1, { align: 'center' });

      // Source title
      doc.setFontSize(11);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(33, 37, 41);
      const titleLines = doc.splitTextToSize(source.title || 'Untitled Source', maxWidth - 15);
      doc.text(titleLines, margin + 12, y);
      y += (titleLines.length * 5) + 3;

      // Reliability badge
      const reliability = source.reliability || 'medium';
      const reliabilityColors: Record<string, [number, number, number]> = {
        high: [40, 167, 69],
        medium: [255, 193, 7],
        low: [108, 117, 125]
      };
      const color = reliabilityColors[reliability] || reliabilityColors.medium;
      doc.setFillColor(color[0], color[1], color[2]);
      doc.roundedRect(margin + 12, y - 4, 25, 7, 2, 2, 'F');
      doc.setFontSize(8);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(255, 255, 255);
      doc.text(reliability.toUpperCase(), margin + 24.5, y + 1, { align: 'center' });
      y += 10;

      // URL
      doc.setFontSize(9);
      doc.setFont('helvetica', 'italic');
      doc.setTextColor(13, 110, 253);
      const urlLines = doc.splitTextToSize(source.url, maxWidth - 15);
      doc.text(urlLines, margin + 12, y);
      y += (urlLines.length * 4) + 10;
    });

    // ========== FOOTER ==========
    const totalPages = doc.getNumberOfPages();
    for (let i = 1; i <= totalPages; i++) {
      doc.setPage(i);
      doc.setFontSize(8);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(150, 150, 150);
      doc.text(`Generated by Deep Research System | Page ${i} of ${totalPages}`, pageWidth / 2, pageHeight - 10, { align: 'center' });
    }

    doc.save(`${title.toLowerCase().replace(/\s+/g, '-')}.pdf`);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full"
    >
      <Card
        title={title}
        subtitle={`${word_count} words • ${sources_used.length} sources`}
        headerAction={
          <div className="flex items-center gap-2">
            <Button variant="secondary" size="sm" onClick={handleDownloadPDF}>
              <FileText className="w-4 h-4 mr-2" />
              PDF
            </Button>
            <Button variant="secondary" size="sm" onClick={handleDownloadMarkdown}>
              <FileCode className="w-4 h-4 mr-2" />
              Markdown
            </Button>
          </div>
        }
      >
        {/* Executive Summary */}
        <div className="mb-6 p-4 bg-slate-800/50 rounded-lg border border-slate-700/50">
          <h4 className="text-sm font-medium text-slate-400 mb-2 uppercase tracking-wider">
            Executive Summary
          </h4>
          <div className="prose prose-invert prose-sm max-w-none">
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{ a: MarkdownLink }}
            >
              {executive_summary}
            </ReactMarkdown>
          </div>
        </div>

        {/* Sections */}
        <div className="space-y-6">
          {sections.map((section, index) => (
            <div key={index} className="border-b border-slate-800 pb-6 last:border-0">
              <h4 className="text-lg font-semibold text-white mb-3">{section.heading}</h4>
              <div className="prose prose-invert prose-sm max-w-none">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{ a: MarkdownLink }}
                >
                  {section.content}
                </ReactMarkdown>
              </div>
            </div>
          ))}
        </div>

        {/* Sources */}
        <div className="mt-8 pt-6 border-t border-slate-800">
          <SourceViewer sources={sources_used} />
        </div>

        {/* Confidence Assessment */}
        <div className="mt-6 p-4 bg-slate-800/30 rounded-lg">
          <h4 className="text-sm font-medium text-slate-400 mb-2">Confidence Assessment</h4>
          <div className="prose prose-invert prose-sm max-w-none">
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{ a: MarkdownLink }}
            >
              {confidence_assessment}
            </ReactMarkdown>
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
